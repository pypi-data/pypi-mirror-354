"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from abc import ABC, abstractmethod
from typing import List

from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)


class IntegrationTestBase(ABC):
    """
    Integration Test Base Class
    """

    def __init__(self, name: str | None = None, index: int = 0):
        self.__name = name
        self.index = index
        self.__config: TestConfiguration = TestConfiguration()
        self.__results: List[IntegrationTestResponse] = []

    @property
    def name(self) -> str:
        """
        Get the name of the test
        """
        return self.__name if self.__name is not None else self.__class__.__name__

    @property
    def config(self) -> TestConfiguration:
        """
        Get the configuration for the test
        """
        if self.__config is None:
            raise RuntimeError(
                "Test configuration not set. "
                "A configuration is required to run integration tests."
            )
        return self.__config

    @config.setter
    def config(self, value: TestConfiguration):
        """
        Set the configuration for the test
        """
        self.__config = value

    @property
    def results(self) -> List[IntegrationTestResponse]:
        """
        Get the results of the test
        """
        return self.__results

    def success(self) -> bool:
        """
        Returns True if all tests in the suite were successful
        """
        return all([result.error is None for result in self.results])

    def skipped_count(self) -> int:
        """
        Gets the number of tests that were skipped
        """
        return len([result for result in self.results if result.skipped])

    def error_count(self) -> int:
        """
        Gets the number of tests that resulted in an error
        """
        return len([result for result in self.results if result.error is not None])

    def errors(self) -> List[str]:
        """
        Gets the list of errors that occurred during the test
        """
        return [result.error for result in self.results if result.error is not None]

    @abstractmethod
    def test(self) -> bool:
        """
        Run the Test
        Args:
            config: The Test Configuration
        Returns:
            True if the test was successful, False otherwise.  If any
            of the tests fail, it will be false.  Execeptions are only
            raised if the raise_on_failure flag is set to True.
        """
        pass
