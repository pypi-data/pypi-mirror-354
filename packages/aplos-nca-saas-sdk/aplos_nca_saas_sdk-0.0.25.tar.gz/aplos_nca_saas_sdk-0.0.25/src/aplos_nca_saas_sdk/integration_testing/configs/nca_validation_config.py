"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict, List

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import (
    LoginConfig,
    LoginConfigs,
)


logger = Logger(service="NCAValidationConfig")


class NCAValidationConfig(ConfigBase):
    """
    NCA Validation Config: Defines an NCA Validation configuration that the application tests will check against

    """

    def __init__(
        self,
        login: LoginConfig,
    ):
        super().__init__()

        if login is None:
            raise RuntimeError("login is required")
        self.__login = login

    @property
    def login(self) -> LoginConfig:
        """Login Configuration"""
        return self.__login


class NCAValidationConfigs(ConfigBase):
    """
    NCA Validation Configs: Defines the configurations that the application NCA Engine tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__list: List[NCAValidationConfig] = []

    @property
    def list(self) -> List[NCAValidationConfig]:
        """List the nca validation configurations"""
        return list(filter(lambda x: x.enabled, self.__list))

    def add(
        self,
        *,
        login: LoginConfig,
        enabled: bool = True,
    ):
        """Add an NCA Validation Config"""
        config = NCAValidationConfig(login)
        config.enabled = enabled
        self.__list.append(config)

    def load(self, test_config: Dict[str, Any]):
        """Loads the NCA Validation configs from a list of dictionaries"""

        super().load(test_config)
        if not self.enabled:
            return

        base_login: LoginConfig | None = LoginConfigs.try_load_login(
            test_config.get("login", None)
        )

        validations: List[Dict[str, Any]] = test_config.get("validations", [])
        for validation in validations:
            enabled = bool(validation.get("enabled", True))
            login: LoginConfig | None = None
            if "login" in validation:
                login = LoginConfigs.try_load_login(validation["login"])
            else:
                login = base_login

            if not login:
                raise RuntimeError("Failed to load the login configuration")

            self.add(
                login=login,
                enabled=enabled,
            )
