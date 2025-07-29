"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from pathlib import Path

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis
from aplos_nca_saas_sdk.utilities.file_utility import FileUtility

logger = Logger(service="NCAAnalysisTest")


class NCAAnalysisTest(IntegrationTestBase):
    """NCA Execution Test Container"""

    def __init__(self):
        super().__init__("nca-execution")

    def test(self) -> bool:
        """Test Engine Execution"""

        self.results.clear()

        for nca_execution_config in self.config.nca_executions.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name

            input_file_path = (
                FileUtility.load_filepath(nca_execution_config.input_file_path),
            )
            logger.info(
                {
                    "message": "Creating NCA Analysis Execution for input file.",
                    "path": input_file_path,
                    "path2": nca_execution_config.input_file_path,
                }
            )
            try:
                # Create new NCA Execution
                nca_execution: NCAAnalysis = NCAAnalysis(
                    nca_execution_config.login.host
                )

                # Initialize Configuration Data

                # Execute, the execution should raise errors that will fail the test
                logger.info({"message": "Invoking Execution"})
                execution_response = nca_execution.execute(
                    username=nca_execution_config.login.username,
                    password=nca_execution_config.login.password,
                    input_file_path=FileUtility.load_filepath(
                        nca_execution_config.input_file_path
                    ),
                    config_data=nca_execution_config.config_data,
                    meta_data=nca_execution_config.meta_data,
                    wait_for_results=nca_execution_config.wait_for_results,
                    max_wait_in_seconds=nca_execution_config.max_wait_in_seconds,
                    output_directory=nca_execution_config.output_dir,
                    unzip_after_download=False,
                    data_processing=nca_execution_config.data_processing,
                    post_processing=nca_execution_config.post_processing,
                    full_payload=nca_execution_config.full_payload,
                )

                # Verify Download
                logger.info(
                    {"message": "Execution complete. Verifying results download."}
                )
                status_code = execution_response.get("results", {}).get("status_code")
                if status_code == 201:
                    pass  # No output file expected
                else:
                    expected_output_file = execution_response.get("results", {}).get("file")
                    if expected_output_file is None:
                        raise RuntimeError(
                            "Expected populated output_file from NCAExecution was None."
                        )
                    elif not Path(expected_output_file).is_file():
                        raise RuntimeError("Expected downloaded file does not exist.")

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()
