"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict
from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass
from aplos_nca_saas_sdk.nca_resources.aws_s3_presigned_upload import (
    S3PresignedUrlUpload,
)


class NCAFileUpload(NCAApiBaseClass):
    """NCA File Upload"""

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
            Dict: {"file_id": id, "statu_code": 204}
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
