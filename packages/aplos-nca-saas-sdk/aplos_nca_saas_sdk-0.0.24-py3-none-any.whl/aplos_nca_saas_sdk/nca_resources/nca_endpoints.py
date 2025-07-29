"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""


class NCAEndpoints:
    """Aplos NCA SaaS Endpoints"""

    def __init__(
        self, *, host: str, tenant_id: str | None = None, user_id: str | None = None
    ):
        self.__host: str = host
        self.__protocal: str = "https://"
        self.tenant_id: str | None = tenant_id
        self.user_id: str | None = user_id

    @property
    def origin(self) -> str:
        """The origin path e.g. https://api.aplos-nca.com"""
        base = f"{self.__protocal}{self.__host}"
        return base

    @property
    def tenant_path(self) -> str:
        """Returns the tenant path"""

        if not self.tenant_id:
            raise ValueError("Missing Tenant Id")

        return f"{self.origin}/tenants/{self.tenant_id}"

    @property
    def user_path(self) -> str:
        """Returns the user path"""

        if not self.user_id:
            raise ValueError("Missing User Id")
        return f"{self.tenant_path}/users/{self.user_id}"

    @property
    def tenant(self) -> str:
        """Returns the tenant endpoint"""
        return f"{self.tenant_path}"

    @property
    def app_configuration(self) -> str:
        """
        Returns the configuration endpoint.  This is a public endpoint.
        """
        return f"{self.origin}/app/configuration"

    @property
    def user(self) -> str:
        """Returns the user endpoint"""
        return f"{self.user_path}"

    @property
    def executions(self) -> str:
        """Returns the executions endpoint"""
        return f"{self.user_path}/nca/executions"

    def execution(self, execution_id: str) -> str:
        """Returns the executions endpoint"""
        return f"{self.executions}/{execution_id}"

    @property
    def validations(self) -> str:
        """Returns the validations endpoint"""
        return f"{self.user_path}/nca/validations"

    def validation(self, batch_id: str) -> str:
        """Returns the validations endpoint for a specific batch"""
        return f"{self.validations}/{batch_id}"

    @property
    def files(self) -> str:
        """Returns the files endpoint"""
        return f"{self.user_path}/nca/files"

    def file(self, file_id: str) -> str:
        """Returns the file endpoint"""
        return f"{self.files}/{file_id}"

    def file_data(self, file_id: str) -> str:
        """Returns get file data endpoint"""
        return f"{self.files}/{file_id}/data"
