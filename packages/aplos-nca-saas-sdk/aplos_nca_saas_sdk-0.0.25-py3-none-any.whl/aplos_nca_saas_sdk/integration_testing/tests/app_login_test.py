"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aplos_nca_saas_sdk.nca_resources.nca_authenticator import NCAAuthenticator


from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)


class TestAppLogin(IntegrationTestBase):
    """Application Configuration Tests"""

    def __init__(self):
        super().__init__("app-login")

    def test(self) -> bool:
        """Test a login"""

        self.results.clear()

        for login in self.config.logins.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            if not login.enabled or not self.config.logins.enabled:
                test_response.skipped = True
                test_response.success = True
                self.results.append(test_response)
                continue
            try:
                nca_login = NCAAuthenticator(host=login.host)
                token = nca_login.authenticate(
                    username=login.username, password=login.password
                )

                if not token:
                    test_response.error = "Failed to authenticate"

                else:
                    test_response.success = True
            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
