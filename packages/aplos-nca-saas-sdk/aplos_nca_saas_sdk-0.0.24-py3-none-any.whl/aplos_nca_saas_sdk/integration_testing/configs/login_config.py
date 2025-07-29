"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Optional, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase


class LoginConfig(ConfigBase):
    """
    Application Login: Defines the login that the application configuration tests will check against

    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        roles: Optional[List[str]] = None,
    ):
        super().__init__()
        self.__username: Optional[str] = username
        self.__password: Optional[str] = password
        self.__host: Optional[str] = host
        self.__roles: List[str] = roles if roles is not None else []

    @property
    def username(self) -> str:
        if self.__username is None:
            raise RuntimeError("Username is not set")
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def password(self) -> str:
        if self.__password is None:
            raise RuntimeError("Password is not set")
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def host(self) -> str:
        """API Host"""
        if self.__host is None:
            raise RuntimeError("Host is not set")
        return self.__host

    @host.setter
    def host(self, value: str):
        self.__host = value

    @property
    def roles(self) -> List[str]:
        """A list of roles to check for"""
        return self.__roles

    @roles.setter
    def roles(self, value: List[str] | None):
        if value is None:
            value = []
        self.__roles = value


class LoginConfigs(ConfigBase):
    """
    Application Logins: Defines the logins that the application configuration tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__logins: List[LoginConfig] = []

    @property
    def list(self) -> List[LoginConfig]:
        """List the logins"""
        return self.__logins

    def add(self, *, username: str, password: str, host: str, enabled: bool = True):
        """Add a loging"""
        login = LoginConfig()
        login.username = username
        login.password = password
        login.host = host
        login.enabled = enabled
        self.__logins.append(login)

    def load(self, test_config: Dict[str, Any]):
        """Load the logins from a list of dictionaries"""

        super().load(test_config)
        if not self.enabled:
            return

        logins: List[Dict[str, str]] = test_config.get("logins", [])
        for login in logins:
            login_config = LoginConfigs.try_load_login(login)
            if login_config is None:
                continue
            self.__logins.append(login_config)

    @staticmethod
    def try_load_login(login_config: Dict[str, Any]) -> LoginConfig | None:
        """Attempts to initialize a Login from a configuration object"""
        login: LoginConfig | None = None
        if login_config is not None:
            username = login_config.get("username", None)
            password = login_config.get("password", None)
            host = login_config.get("host", None)
            enabled = login_config.get("enabled", True)
            login = LoginConfig(username, password, host)
            login.enabled = enabled
        return login
