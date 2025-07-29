"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase


class ApplicationHostConfig(ConfigBase):
    """
    Application host: Defines the hosts that the application configuration tests will check against

    """

    def __init__(self, host: str | None = None):
        super().__init__()
        self.__host: str | None = host

    @property
    def host(self) -> str:
        """The host to validate"""
        if self.__host is None:
            raise RuntimeError("host is not set")
        return self.__host

    @host.setter
    def host(self, value: str):
        self.__host = value


class ApplicationHostConfigs(ConfigBase):
    """
    Application ApplicationHost: Defines the hosts that the application configuration tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__hosts: List[ApplicationHostConfig] = []

    @property
    def list(self) -> List[ApplicationHostConfig]:
        """List the logins"""
        return self.__hosts

    def add(self, *, host: str, enabled: bool = True):
        """Add a loging"""
        app_domain = ApplicationHostConfig()
        app_domain.host = host
        app_domain.enabled = enabled
        self.__hosts.append(app_domain)

    def load(self, test_config: Dict[str, Any]):
        """Load the logins from a list of dictionaries"""
        # self.enabled = bool(test_config.get("enabled", True))
        super().load(test_config)
        hosts: List[Dict[str, Any]] = test_config.get("hosts", [])

        host: Dict[str, Any]
        for host in hosts:
            app_domain = ApplicationHostConfig()
            app_domain.host = host.get("host", None)
            app_domain.enabled = bool(host.get("enabled", True))

            self.__hosts.append(app_domain)


class ApplicationSettings(ConfigBase):
    """
    Application Settings: Defines the hosts that the application settings (configuration endpoint) tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__hosts: ApplicationHostConfigs = ApplicationHostConfigs()

    @property
    def hosts(self) -> ApplicationHostConfigs:
        """List of the host"""
        return self.__hosts

    def load(self, test_config: Dict[str, Any]):
        """Load the hosts from the config"""
        super().load(test_config)
        if not self.enabled:
            return
        self.hosts.load(test_config)
