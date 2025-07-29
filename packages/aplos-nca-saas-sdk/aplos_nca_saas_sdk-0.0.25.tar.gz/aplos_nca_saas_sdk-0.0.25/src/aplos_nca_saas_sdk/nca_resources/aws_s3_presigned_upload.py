"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
import os
from typing import Any, Dict

import requests
from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_payload import (
    S3PresignedUrlPayload,
)
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities
from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass


class S3PresignedUrlUpload(NCAApiBaseClass):
    """S3PresignedUrlUpload"""

    def __init__(self, host: str) -> None:
        super().__init__(host)

    def upload_file(
        self,
        input_file: str,
    ) -> Dict[str, Any]:
        """
        Uploads a file to your Aplos Cloud Account in AWS

        Args:
            input_file (str): path to the analysis file you are uploading

        Returns:
            Dictionary: including the file_id, status code and response information
        """

        # get the presigned url for uploading
        paylod: S3PresignedUrlPayload = self.__get_presigned_upload_info(
            input_file=input_file, jwt=self.authenticator.cognito.jwt
        )
        # upload the files
        upload_response = self.__upload_file_to_s3(paylod, input_file=input_file)

        return upload_response

    def __get_presigned_upload_info(
        self, input_file: str, jwt: str
    ) -> S3PresignedUrlPayload:
        """
        Performs all the necessary steps for creating a presigned url to upload a file to S3.
        We're using AWS S3 presigned urls for security as well as allowing for very large files if required.
        Args:
            input_file (str): the path to the input (analysis) file

        Returns:
            S3PresignedUrlPayload: instance of S3PresignedUrlPayload
        """

        url = self.endpoints.files
        headers = HttpUtilities.get_headers(jwt)

        body = {"file_name": input_file, "method_type": "post"}
        response = requests.post(
            url=url, headers=headers, data=json.dumps(body), timeout=30
        )

        if response.status_code == 403:
            raise PermissionError(
                "Failed to get a presigned url. "
                f"Status Code: {response.status_code}"
                f"Reason: {response.reason} "
                f"403 Errors can also occur if you have an invalid path."
            )
        elif response.status_code != 200:
            raise RuntimeError(
                "Failed to get a presigned url. "
                f"Status Code: {response.status_code}"
                f"Reason: {response.reason}"
            )
        result = response.json()

        payload: S3PresignedUrlPayload = S3PresignedUrlPayload(result)

        return payload

    def __upload_file_to_s3(
        self, payload: S3PresignedUrlPayload, input_file: str
    ) -> Dict[str, Any]:
        """
        Peforms the actual uploading via a presigned url for S3 bucket storage
        Args:
            payload (S3PresignedUrlPayload): instance of S3PresignedUrlPayload with all the data needed
            input_file (str): the path to a file being uploaded

        Raises:
            FileNotFoundError: If the file is not found

        Returns:
            bool: True on success, False if not
        """

        if not os.path.exists(input_file):
            raise FileNotFoundError(
                "The input file you are submitting cannot be found.  Please check the path and try again."
            )

        with open(input_file, "rb") as file:
            files = {"file": (input_file, file)}
            # upload to s3 with the presigned url
            # authentication is built into the url
            upload_response = requests.post(
                str(payload.url), data=payload.form_data, files=files, timeout=60
            )

        # Check the response: 204 is a success in this case
        if upload_response and upload_response.status_code == 204:
            return {
                "status_code": upload_response.status_code,
                "reason": upload_response.reason,
                "details": "File uploaded successfully. Post-Processing will being soon.",
                "file_id": payload.file_id,
            }
        else:
            raise RuntimeError(
                "Error uploading the file. "
                f"Status Code: {upload_response.status_code}"
                f"Response: {upload_response.reason}"
            )
