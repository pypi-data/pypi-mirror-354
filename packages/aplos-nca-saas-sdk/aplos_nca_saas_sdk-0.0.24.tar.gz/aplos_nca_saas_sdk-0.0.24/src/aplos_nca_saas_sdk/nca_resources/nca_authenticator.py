"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Optional
from aplos_nca_saas_sdk.nca_resources.aws_cognito import CognitoAuthentication
from aplos_nca_saas_sdk.nca_resources.nca_app_configuration import (
    NCAAppConfiguration,
)
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities


class NCAAuthenticator:
    """NCA Authenticator"""

    def __init__(
        self,
        *,
        cognito_client_id: Optional[str] = None,
        cognito_region: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        """
        NCA SaaS Login

        Args:
            cognito_client_id (Optional[str], optional): Cognito Client Id. Defaults to None.
            cognito_region (Optional[str], optional): Cognito Region. Defaults to None.
            host (Optional[str], optional): Aplos NCA SaaS host. Defaults to None.

        Requirements:
            Either pass in the cognito_client_id and cognito_region.
            or set the host to automatically get the client_id and region.
        """

        self.__cognito_client_id = cognito_client_id
        self.__region = cognito_region
        self.__host: Optional[str] = host
        self.__cognito: Optional[CognitoAuthentication] = None
        self.__config: Optional[NCAAppConfiguration] = None

    @property
    def cognito(self) -> CognitoAuthentication:
        """
        Cognito Authentication
        Returns:
            CognitoAuthenication: object to handle cognito authentication
        """
        if self.__cognito is None:
            self.__cognito = CognitoAuthentication(
                client_id=self.__cognito_client_id,
                region=self.__region,
                aplos_domain=self.__host,
            )

        return self.__cognito

    @property
    def host(self) -> str | None:
        """
        Domain
        Returns:
            str: the host
        """
        return self.__host

    @property
    def config(self) -> NCAAppConfiguration:
        """
        NCA App Configuration
        Returns:
            NCAAppConfiguration: object to handle the NCA App Configuration
        """
        if self.__config is None:
            if self.__host is None:
                raise RuntimeError(
                    "Failed to get Aplos Configuration.  The Domain is not set."
                )

            self.__config = NCAAppConfiguration(
                host=self.__host,
            )

        return self.__config

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> str:
        """_summary_

        Args:
            username (str): the username
            password (str): the users password
        Returns:
            str: JWT (JSON Web Token)
        """
        if not username:
            raise ValueError("Missing username.  Please provide a valid username.")
        if not password:
            raise ValueError("Missing password.  Please provide a valid password.")

        self.cognito.login(username=username, password=password)

        return self.cognito.jwt

    def get_jwt_http_headers(self) -> str:
        """Get the formatted http headers for the JWT"""
        return HttpUtilities.get_headers(self.cognito.jwt)
