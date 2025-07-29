"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from typing import List, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import (
    LoginConfig,
    LoginConfigs,
)

from aplos_nca_saas_sdk.utilities.file_utility import FileUtility


class FileUploadConfig(ConfigBase):
    """
    File Upload: Defines the login that the application configuration tests will check against

    """

    def __init__(self, login: LoginConfig, file_path: str):
        super().__init__()
        if login is None:
            raise RuntimeError("Login is required")
        self.__login = login
        if file_path is None:
            raise RuntimeError("file_path is required")
        self.__filepath = file_path

    @property
    def login(self) -> LoginConfig:
        """The users login"""
        return self.__login

    @property
    def file_path(self) -> str:
        """The file path to file being uploaded"""
        path = FileUtility.load_filepath(self.__filepath)

        if not os.path.exists(path):
            raise RuntimeError(f"The Upload File was not found: {path}")

        return path


class FileUploadConfigs(ConfigBase):
    """
    File Uploads: Defines the files that the application file upload tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__fileuploads: List[FileUploadConfig] = []

    @property
    def list(self) -> List[FileUploadConfig]:
        """List the file uploads"""
        return list(filter(lambda x: x.enabled, self.__fileuploads))

    def add(self, *, file_path: str, login: LoginConfig, enabled: bool = True):
        """Add a file upload"""
        file_upload = FileUploadConfig(login, file_path)
        file_upload.enabled = enabled
        self.__fileuploads.append(file_upload)

    def load(self, test_config: Dict[str, Any]):
        """Load the file uploads from a list of dictionaries"""

        super().load(test_config)
        if not self.enabled:
            return

        test_config_login: LoginConfig | None = LoginConfigs.try_load_login(
            test_config.get("login", None)
        )
        file_uploads: List[Dict[str, Any]] = test_config.get("files", [])
        login: LoginConfig | None = None
        for file_upload in file_uploads:
            enabled = bool(file_upload.get("enabled", True))
            if "login" in file_upload:
                login = LoginConfigs.try_load_login(file_upload["login"])
            else:
                login = test_config_login

            file_path = file_upload.get("file", None)

            if not file_path:
                raise RuntimeError("file_path is required")

            if not login:
                raise RuntimeError("login configuration is required")

            self.add(file_path=file_path, login=login, enabled=enabled)
