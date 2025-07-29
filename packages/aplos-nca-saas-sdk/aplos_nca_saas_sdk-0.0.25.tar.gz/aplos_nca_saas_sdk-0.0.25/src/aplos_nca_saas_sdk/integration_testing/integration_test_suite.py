"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from datetime import datetime, UTC
from aws_lambda_powertools import Logger
from aplos_nca_saas_sdk.integration_testing.integration_test_factory import (
    IntegrationTestFactory,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)

logger = Logger(service="IntegrationTestSuite")


class IntegrationTestSuite:
    """Runs Tests against an active instance"""

    def __init__(self):
        self.test_results: List[Dict[str, Any]] = []
        self.verbose: bool = False
        self.raise_on_failure: bool = False
        self.fail_fast: bool = False

    def test(self, test_config: TestConfiguration) -> bool:
        """Run a full suite of integration tests"""

        # reset the test results
        self.test_results = []

        start_time: datetime = datetime.now(UTC)
        factory: IntegrationTestFactory = IntegrationTestFactory()
        test: IntegrationTestBase | None = None
        for test in factory.test_instances:
            test.config = test_config
            test_result: Dict[str, Any] = {
                "test_name": test.name,
                "success": 0,
                "errors": [],
                "skipped_count": 0,
                "error_count": 0,
                "start_time_utc": None,
                "end_time_utc": None,
            }

            logger.info(f"Running test class {test.name}")
            try:
                test_result["start_time_utc"] = datetime.now(UTC)
                success = test.test()
                test_result["success"] = success
                test_result["results"] = test.results
                test_result["skipped_count"] = test.skipped_count()
                test_result["error_count"] = test.error_count()
                test_result["errors"] = test.errors()
                if not success:
                    if self.fail_fast:
                        # just break and let the failure routine handle it
                        break

            except Exception as e:  # pylint: disable=broad-except
                test_result["success"] = False
                test_result["errors"] = [str(e)]
                if self.fail_fast:
                    # just break and let the failure routine handle it
                    break
            finally:
                test_result["end_time_utc"] = datetime.now(UTC)
                self.test_results.append(test_result)

                if test_result["success"]:
                    logger.info(f"Test {test.name} succeeded")
                    logger.debug(test_result)
                else:
                    logger.error(test_result)
        # find the failures
        failures = [test for test in self.test_results if len(test["errors"]) > 0]
        self.__print_results(start_time, failures)

        # print the results

        if self.raise_on_failure and len(failures) > 0:
            count = len(failures)
            logger.error(f"{count} tests failed. Raising exception.")
            raise RuntimeError(f"{count} tests failed")

        return len(failures) == 0

    def __print_results(self, start_time: datetime, failures: List[Dict[str, Any]]):
        print("")
        print("--------------------------------")
        print("Test Results:")
        skipped = sum([test["skipped_count"] for test in self.test_results])

        for test_result in self.test_results:
            duration = test_result["end_time_utc"] - test_result["start_time_utc"]
            print(
                f"  {test_result['test_name']} {'succeeded' if test_result['success'] else 'failed'} duration: {duration}"
            )

        print(f"Test Suite completed in {datetime.now(UTC) - start_time}")

        print(f"  Total Tests: {len(self.test_results)}")
        print(f"  Successful: {len(self.test_results) - len(failures) - skipped}")
        print(f"  Skipped: {skipped}")
        print(f"  Failed: {len(failures)}")

        if len(failures) > 0:
            print("--------------------------------")

        for test_result in self.test_results:
            if not test_result["success"]:
                print(f"Errors: {test_result['errors']}")
