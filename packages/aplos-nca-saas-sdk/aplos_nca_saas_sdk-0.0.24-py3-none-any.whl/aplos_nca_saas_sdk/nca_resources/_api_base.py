"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any


from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator
from aplos_nca_saas_sdk.nca_resources.nca_endpoints import NCAEndpoints


class NCAApiBaseClass:
    """NCA Api Base Class"""

    def __init__(self, host: str) -> None:
        self.host = host
        self.__authenticator: NCAAuthenticator = NCAAuthenticator(host=host)
        self.__endpoints: NCAEndpoints = NCAEndpoints(host=host)
        if not host:
            raise ValueError("Missing Aplos Api Domain")

    @property
    def authenticator(self) -> NCAAuthenticator:
        """Gets the authenticator"""

        return self.__authenticator

    @authenticator.setter
    def authenticator(self, value: Any) -> None:
        """Sets the authenticator"""

        self.__authenticator = value

    @property
    def endpoints(self) -> NCAEndpoints:
        """Gets the endpoints"""

        if self.authenticator.cognito.jwt:
            self.__endpoints.tenant_id = self.authenticator.cognito.tenant_id
            self.__endpoints.user_id = self.authenticator.cognito.user_id

        return self.__endpoints
