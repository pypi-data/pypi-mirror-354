"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_validations import NCAValidation


logger = Logger(service="NCAAnalysisValidationTest")


class NCAAnalysisValidationTest(IntegrationTestBase):
    """NCA Validation Test Container"""

    def __init__(self):
        super().__init__("nca-validation")

    def test(self) -> bool:
        """Test Engine Validation"""

        self.results.clear()

        for config in self.config.nca_validations.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name

            try:
                # Create new NCA Execution
                nca_validation: NCAValidation = NCAValidation(config.login.host)

                # Initialize Configuration Data

                # Execute, the execution should raise errors that will fail the test
                logger.info({"message": "Invoking Execution"})
                execution_response = nca_validation.execute(
                    username=config.login.username,
                    password=config.login.password,
                    wait_for_results=True,
                )

                # Verify Download
                logger.info({"message": "Validation complete. Verifying results."})

                pass_fail = execution_response.get("results", {}).get("pass_fail")
                if pass_fail != "pass":
                    raise RuntimeError("One or more validations failed.")

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
