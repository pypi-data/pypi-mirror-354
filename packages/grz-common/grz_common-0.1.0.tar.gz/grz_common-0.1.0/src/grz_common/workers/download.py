"""Module for downloading encrypted submissions to local storage"""

from __future__ import annotations

import datetime
import itertools
import logging
import math
import re
from operator import attrgetter, itemgetter
from os import PathLike
from pathlib import Path
from typing import TYPE_CHECKING

import botocore.handlers
from boto3.s3.transfer import S3Transfer, TransferConfig  # type: ignore[import-untyped]
from pydantic import BaseModel
from tqdm.auto import tqdm

from ..constants import TQDM_SMOOTHING
from ..models.s3 import S3Options
from ..progress import DownloadState, FileProgressLogger
from ..transfer import init_s3_client

MULTIPART_THRESHOLD = 8 * 1024 * 1024  # 8MiB, boto3 default
MULTIPART_CHUNKSIZE = 8 * 1024 * 1024  # 8MiB, boto3 default
MULTIPART_MAX_CHUNKS = 1000  # CEPH S3 limit, AWS limit is 10000

if TYPE_CHECKING:
    from .submission import EncryptedSubmission

log = logging.getLogger(__name__)

# see discussion: https://github.com/boto/boto3/discussions/4251 to accept bucket names with ":" in the name
botocore.handlers.VALID_BUCKET = re.compile(r"^[:a-zA-Z0-9.\-_]{1,255}$")


class DownloadError(Exception):
    """Exception raised when an upload fails"""

    pass


class S3BotoDownloadWorker:
    """Implementation of an upload worker using boto3 for S3"""

    __log = log.getChild("S3BotoDownloadWorker")

    def __init__(
        self,
        s3_options: S3Options,
        status_file_path: str | PathLike,
        threads: int = 1,
    ):
        """
        An download manager for S3 storage

        :param config: The configuration model
        :param status_file_path: The path to the status file
        """
        super().__init__()

        self._status_file_path = Path(status_file_path)
        self._s3_options = s3_options
        self._threads = threads

        self._s3_client = init_s3_client(s3_options)

    def prepare_download(
        self,
        metadata_dir: Path,
        encrypted_files_dir: Path,
        log_dir: Path,
    ):
        """
        Prepare the download of an encrypted submission

        :param metadata_dir: Path to the metadata directory
        :param encrypted_files_dir: Path to the encrypted_files directory
        :param log_dir: Path to the logs directory
        """
        for dir_path in [metadata_dir, encrypted_files_dir, log_dir]:
            if not dir_path.exists():
                self.__log.debug("Creating directory: %s", dir_path)
                dir_path.mkdir(parents=False, exist_ok=False)  # Create the directories
            else:
                self.__log.debug("Directory exists: %s", dir_path)

    def download_metadata(
        self,
        submission_id: str,
        metadata_dir: Path,
        metadata_file_name: str = "metadata.json",
    ):
        """
        Download the metadata.json

        :param submission_id: submission folder on S3 structure
        :param metadata_dir: Path of the metadir folder
        :param metadata_file_name: name of the metadata.json
        """
        metadata_key = str(Path(submission_id) / metadata_dir.name / metadata_file_name)
        metadata_file_path = metadata_dir / metadata_file_name

        try:
            self.download_file(str(metadata_file_path), metadata_key, 10000)
        except Exception as e:
            self.__log.error("Download failed for '%s'", str(metadata_key))

            raise e

    def download_file(self, local_file_path, s3_object_id, filesize):
        """
        Upload a single file to the specified object ID
        :param local_file_path: Path to the file to upload
        :param s3_object_id: Remote S3 object ID under which the file should be stored
        :param filesize: size of the file
        """
        # self.__log.info(f"Download {s3_object_id} to {local_file_path}...")

        chunksize = (
            math.ceil(filesize / MULTIPART_MAX_CHUNKS)
            if filesize / MULTIPART_CHUNKSIZE > MULTIPART_MAX_CHUNKS
            else MULTIPART_CHUNKSIZE
        )
        self.__log.debug(f"Using a chunksize of: {chunksize / 1024**2}MiB, results in {filesize / chunksize} chunks")

        config = TransferConfig(
            multipart_threshold=MULTIPART_THRESHOLD,
            multipart_chunksize=chunksize,
            max_concurrency=self._threads,
        )

        transfer = S3Transfer(self._s3_client, config)
        progress_bar = tqdm(total=filesize, unit="B", unit_scale=True, unit_divisor=1024, smoothing=TQDM_SMOOTHING)
        transfer.download_file(
            self._s3_options.bucket,
            s3_object_id,
            local_file_path,
            callback=lambda bytes_transferred: progress_bar.update(bytes_transferred),
        )

    def download(self, submission_id: str, encrypted_submission: EncryptedSubmission):
        """
        Upload an encrypted submission
        :param encrypted_submission: The encrypted submission to upload
        """
        progress_logger = FileProgressLogger[DownloadState](self._status_file_path)

        encrypted_files_key_prefix = f"{submission_id}/files/"

        response = self._s3_client.list_objects_v2(Bucket=self._s3_options.bucket, Prefix=encrypted_files_key_prefix)

        if "Contents" in response:
            for file in response["Contents"]:
                if file["Size"] == 0:
                    continue
                else:
                    file_key = file["Key"]
                    file_path = Path(file_key).relative_to(encrypted_files_key_prefix)
                    full_path = encrypted_submission.encrypted_files_dir / file_path
                    if full_path not in encrypted_submission.encrypted_files:
                        raise DownloadError(f"File {file_path} not listed in metadata.json")
                    file_metadata = encrypted_submission.encrypted_files[full_path]
                    logged_state = progress_logger.get_state(full_path, file_metadata)

                    if (logged_state is None) or not logged_state.get("download_successful", False):
                        self.__log.info(
                            "Download file: '%s' -> '%s'",
                            file_key,
                            str(full_path),
                        )

                        try:
                            full_path.parent.mkdir(mode=0o770, parents=True, exist_ok=True)
                            self.download_file(str(full_path), file_key, file["Size"])

                            self.__log.info(f"Download complete for {str(full_path)}. ")
                            progress_logger.set_state(
                                full_path,
                                file_metadata,
                                state=DownloadState(download_successful=True),
                            )
                        except Exception as e:
                            self.__log.error("Download failed for '%s'", str(full_path))

                            progress_logger.set_state(
                                full_path,
                                file_metadata,
                                state=DownloadState(download_successful=False, errors=[str(e)]),
                            )

                            raise e
                    else:
                        self.__log.info(
                            "File '%s' already downloaded (at '%s')",
                            file_key,
                            str(full_path),
                        )


class SubmissionInboxState(BaseModel):
    """A summary of the state of a submission in an inbox"""

    submission_id: str
    complete: bool
    oldest_upload: datetime.datetime
    newest_upload: datetime.datetime


def query_submissions(s3_options: S3Options) -> list[SubmissionInboxState]:
    """Queries the state of all submissions in the configured bucket."""
    s3_client = init_s3_client(s3_options)
    paginator = s3_client.get_paginator("list_objects_v2")

    objects = itertools.chain.from_iterable(
        page["Contents"] for page in paginator.paginate(Bucket=s3_options.bucket) if "Contents" in page
    )
    objects_sorted = sorted(objects, key=itemgetter("Key"))  # pyrefly: ignore
    submission2objects = {
        key: tuple(group) for key, group in itertools.groupby(objects_sorted, key=lambda o: o["Key"].split("/")[0])
    }

    submissions = []
    for submission_id, submission_objects in submission2objects.items():
        submission_objects_sorted = sorted(submission_objects, key=itemgetter("LastModified"))  # pyrefly: ignore
        oldest_object = submission_objects_sorted[0]
        newest_object = submission_objects_sorted[-1]
        is_complete = len(list(filter(lambda o: o["Key"].endswith("/metadata.json"), submission_objects))) == 1
        submission = SubmissionInboxState(
            submission_id=submission_id,
            complete=is_complete,
            oldest_upload=oldest_object["LastModified"],
            newest_upload=newest_object["LastModified"],
        )
        submissions.append(submission)

    return sorted(submissions, key=attrgetter("oldest_upload"))  # pyrefly: ignore
