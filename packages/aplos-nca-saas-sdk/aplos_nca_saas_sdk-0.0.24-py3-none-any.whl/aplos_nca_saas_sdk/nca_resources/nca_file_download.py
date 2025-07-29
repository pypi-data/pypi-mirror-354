"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests
from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_upload import (
    S3PresignedUrlUpload,
)
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities

logger = Logger(service="nca-file-download")


class NCAFileDownload(NCAApiBaseClass):
    """NCA File Download"""

    def __init__(self, host: str) -> None:
        super().__init__(host)

    def upload(
        self,
        input_file_path: str,
        user_name: str | None = None,
        password: str | None = None,
    ) -> Dict[str, Any]:
        """
        Uploads a file to the Aplos NCA Cloud

        Args:
            input_file_path (str): local path to the file

        Raises:
            ValueError: _description_

        Returns:
            Dict: {"file_id": id, "status_code": 204, ...}
            204 Response staus_code is a success
        """
        if input_file_path is None or not input_file_path:
            raise ValueError("Valid input_file_path is required.")

        if not self.authenticator.cognito.jwt:
            if not user_name or not password:
                raise ValueError(
                    "Valid user_name and password are required or you can set the authenticator object."
                )
            self.authenticator.authenticate(username=user_name, password=password)

        uploader: S3PresignedUrlUpload = S3PresignedUrlUpload(self.host)
        uploader.authenticator = self.authenticator

        upload_response: Dict[str, Any] = uploader.upload_file(
            input_file=input_file_path
        )

        return upload_response

    def download(
        self,
        file_id: str,
        user_name: str | None = None,
        password: str | None = None,
        wait_time_in_seconds: float = 5,
        max_tries: float = 12,
        required_workable_state: str = "ready",
    ) -> Dict[str, Any]:
        """
        Downloads a file from the Aplos NCA Cloud

        Args:
            file_id (str): the id of the file to download
            user_name Optional(str): the username used to connect.  If not specified
                the authenticator is required.
            password Optional(str): the password used to connect.  If not specified
                the authenticator is required.

        Raises:
            ValueError: _description_

        Returns:
            Dict: {"file_id": id, "statu_code": 204}
        """

        logger.info({"message": "Downloading file", "file_id": file_id})

        file_info_endpoint = self.endpoints.file(
            file_id,
        )

        if not self.authenticator.cognito.jwt:
            if not user_name or not password:
                raise ValueError(
                    "Valid user_name and password are required or you can set the authenticator object."
                )
            self.authenticator.authenticate(username=user_name, password=password)

        headers = HttpUtilities.get_headers(self.authenticator.cognito.jwt)
        current_time = datetime.now()

        if max_tries < 0:
            max_tries = 1
        if wait_time_in_seconds < 0:
            wait_time_in_seconds = 1

        max_wait_time_in_seconds = wait_time_in_seconds * max_tries
        # Create a timedelta object representing x seconds
        time_delta = timedelta(seconds=max_wait_time_in_seconds)
        # Add the timedelta to the current time
        max_time = current_time + time_delta

        complete = False
        json_response: Dict[str, Any] = {}
        while not complete:
            response = requests.get(file_info_endpoint, headers=headers, timeout=60)
            json_response: dict = response.json()
            errors: List[Dict[str, Any]] = []
            errors.extend(json_response.get("errors") or [])
            status = json_response.get("workable_state")
            complete = status == "ready"

            if not required_workable_state or required_workable_state == "any":
                break
            if status == "invalid" or len(errors) > 0:
                break
            if complete:
                break
            if not complete:
                time.sleep(wait_time_in_seconds)
            if datetime.now() > max_time:
                error = (
                    "Timeout attempting to get an analysis file. "
                    f"The current timeout limit is {max_wait_time_in_seconds} seconds. "
                    "You may need to up the timeout period, or check for errors. "
                )
                raise RuntimeError(error)

        return json_response
