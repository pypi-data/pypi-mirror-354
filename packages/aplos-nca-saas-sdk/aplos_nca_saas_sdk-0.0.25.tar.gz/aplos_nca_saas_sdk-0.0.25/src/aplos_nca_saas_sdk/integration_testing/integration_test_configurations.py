"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
from typing import Any, Dict
from aplos_nca_saas_sdk.integration_testing.configs.app_settings_config import (
    ApplicationSettings,
)
from aplos_nca_saas_sdk.integration_testing.configs.file_upload_config import (
    FileUploadConfigs,
)
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfigs
from aplos_nca_saas_sdk.integration_testing.configs.nca_execution_config import (
    NCAExecutionConfigs,
)

from aplos_nca_saas_sdk.integration_testing.configs.nca_validation_config import (
    NCAValidationConfigs,
)


class TestConfiguration:
    """
    Testing Suite Configuration: Provides a way to define the testing configuration for the Aplos Analytics SaaS SDK

    """

    def __init__(self):
        self.app_config: ApplicationSettings = ApplicationSettings()
        self.logins: LoginConfigs = LoginConfigs()
        self.file_uploads: FileUploadConfigs = FileUploadConfigs()
        self.nca_executions: NCAExecutionConfigs = NCAExecutionConfigs()
        self.nca_validations: NCAValidationConfigs = NCAValidationConfigs()

    def load(self, file_path: str):
        """
        Loads the configuration from a file

        :param file_path: The path to the configuration file
        :return: None
        """

        config: Dict[str, Any] = {}
        with open(file_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.logins.load(config.get("login_test", {}))
        self.app_config.load(config.get("application_config_test", {}))
        self.file_uploads.load(config.get("file_upload_test", {}))
        self.nca_executions.load(config.get("analysis_execution_test", {}))
        self.nca_validations.load(config.get("analysis_validation_test", {}))
