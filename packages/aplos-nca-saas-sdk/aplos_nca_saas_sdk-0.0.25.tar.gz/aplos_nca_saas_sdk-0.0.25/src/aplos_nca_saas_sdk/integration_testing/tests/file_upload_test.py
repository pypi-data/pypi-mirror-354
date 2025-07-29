"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
from typing import Any, Dict

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.configs.file_upload_config import (
    FileUploadConfig,
)
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfig
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator
from aplos_nca_saas_sdk.nca_resources.nca_file_download import NCAFileDownload
from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload

logger = Logger()


class FileUploadTest(IntegrationTestBase):
    """File Upload Test Container"""

    def __init__(self):
        super().__init__("file-upload")

    def test(self) -> bool:
        """Test file upload"""

        self.results.clear()

        file_upload: FileUploadConfig
        for file_upload in self.config.file_uploads.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            try:
                # Confirm Login
                nca_login = self.__login(file_upload.login)

                # Confirm Upload
                upload_response: Dict[str, Any] = self.__upload(
                    nca_login, file_upload.file_path
                )
                if upload_response is None:
                    test_response.error = "Failed to upload"
                else:
                    # Confirm conversion and download
                    # Allow time buffer so file data is available
                    file_id: str = upload_response.get("file_id", "")
                    if not file_id:
                        raise RuntimeError("Failed to get a file_id from the upload")
                    time.sleep(3)
                    self.__download(nca_login, file_id, test_response)

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()

    def __login(self, login: LoginConfig) -> NCAAuthenticator:
        nca_login = NCAAuthenticator(host=login.host)
        nca_login.authenticate(username=login.username, password=login.password)
        return nca_login

    def __upload(self, auth: NCAAuthenticator, upload_file_path: str) -> Dict[str, Any]:
        logger.info({"message": "Uploading file", "file_path": upload_file_path})

        nca_file_upload = NCAFileUpload(auth.host)
        nca_file_upload.authenticator = auth
        upload_response: Dict[str, Any] = nca_file_upload.upload(upload_file_path)
        return upload_response

    def __download(
        self,
        nca_login: NCAAuthenticator,
        file_id: str,
        test_response: IntegrationTestResponse,
    ):
        logger.info({"message": "Downloading file", "file_id": file_id})
        downloader: NCAFileDownload = NCAFileDownload(nca_login.host)
        downloader.authenticator = nca_login
        response = downloader.download(file_id)

        status = response.get("workable_state")
        if status != "ready":
            test_response.success = False
            test_response.error = f"File conversion failed. Status: {status}"
        else:
            test_response.success = True

        test_response.response = response

        return response
