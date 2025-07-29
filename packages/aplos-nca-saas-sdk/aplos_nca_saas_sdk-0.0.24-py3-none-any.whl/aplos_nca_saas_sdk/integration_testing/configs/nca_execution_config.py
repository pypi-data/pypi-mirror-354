"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
import os
from typing import Any, Dict, List

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import (
    LoginConfig,
    LoginConfigs,
)
from aplos_nca_saas_sdk.utilities.file_utility import FileUtility

logger = Logger(service="NCAExecutionConfig")


class NCAExecutionConfig(ConfigBase):
    """
    NCA Execution Config: Defines an NCA Execution configuration that the application execution tests will check against

    """

    def __init__(
        self,
        login: LoginConfig,
        input_file_path: str,
        config_data: dict,
        meta_data: str | dict | None = None,
        output_dir: str | None = None,
        unzip_after_download: bool = False,
        data_processing: str | dict | None = None,
        post_processing: str | dict | None = None,
        full_payload: str | dict | None = None,
        wait_for_results: bool = True,
        max_wait_in_seconds: int = 600,
        enabled: bool = True
    ):
        super().__init__()

        if login is None:
            raise RuntimeError("login is required")
        self.__login = login

        if input_file_path is None:
            raise RuntimeError("input_file_path is required")
        self.__input_file_path = input_file_path

        if config_data is None:
            raise RuntimeError("config_data is required")
        self.__config_data = config_data

        self.__meta_data = meta_data
        self.__output_dir = output_dir
        self.__unzip_after_download = unzip_after_download
        self.__data_processing = data_processing
        self.__post_processing = post_processing
        self.__full_payload = full_payload
        self.wait_for_results = wait_for_results
        self.max_wait_in_seconds = max_wait_in_seconds
        self.enabled = enabled

    @property
    def login(self) -> LoginConfig:
        """Login Configuration"""
        return self.__login

    @property
    def input_file_path(self) -> str:
        """Input File Path"""
        return self.__input_file_path

    @property
    def config_data(self) -> Dict[str, Any]:
        """Config Data"""
        return self.__config_data

    @property
    def meta_data(self) -> str | Dict[str, Any] | None:
        """Optional Meta Data"""
        return self.__meta_data

    @property
    def output_dir(self) -> str | None:
        """Local Output Directory"""
        return self.__output_dir

    @property
    def unzip_after_download(self) -> bool:
        """Indicates if the download should be unzipped"""
        return self.__unzip_after_download

    @property
    def data_processing(self) -> str | Dict[str, Any] | None:
        """Pre Processing"""
        return self.__data_processing
    
    @property
    def post_processing(self) -> str | Dict[str, Any] | None:
        """Post Processing"""
        return self.__post_processing
    
    @property
    def full_payload(self) -> str | Dict[str, Any] | None:
        """Full Payload"""
        return self.__full_payload

class NCAExecutionConfigs(ConfigBase):
    """
    NCA Execution Configs: Defines the configurations that the application NCA Engine tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__nca_executions: List[NCAExecutionConfig] = []

    @property
    def list(self) -> List[NCAExecutionConfig]:
        """List the nca execution configurations"""
        return list(filter(lambda x: x.enabled, self.__nca_executions))

    def add(
        self,
        *,
        login: LoginConfig,
        input_file_path: str,
        config_data: dict,
        meta_data: str | dict | None = None,
        data_processing: str | dict | None = None,
        post_processing: str | dict | None = None,
        output_dir: str | None = None,
        unzip_after_download: bool = False,
        enabled: bool = True,
        full_payload: str | dict | None = None,
        wait_for_results: bool = True,
        max_wait_in_seconds: int = 600
    ):
        """Add an NCA Execution Config"""
        nca_execution_config = NCAExecutionConfig(
            login,
            input_file_path,
            config_data,
            meta_data,
            output_dir,
            unzip_after_download,
            data_processing,
            post_processing,
            full_payload,
            wait_for_results=wait_for_results,
            max_wait_in_seconds=max_wait_in_seconds
        )
        nca_execution_config.enabled = enabled
        self.__nca_executions.append(nca_execution_config)

    def load(self, test_config: Dict[str, Any]):
        """Loads the NCA Execution configs from a list of dictionaries"""

        super().load(test_config)
        if not self.enabled:
            return

        base_login: LoginConfig | None = LoginConfigs.try_load_login(
            test_config.get("login", None)
        )
        base_output_dir: str = test_config.get("output_dir", None)
        analyses: List[Dict[str, Any]] = test_config.get("analyses", [])
        for analysis in analyses:
            enabled = bool(analysis.get("enabled", True))
            login: LoginConfig | None = None
            if "login" in analysis:
                login = LoginConfigs.try_load_login(analysis["login"])
            else:
                login = base_login

            if "output_dir" in analysis:
                output_dir = analysis["output_dir"]
            else:
                output_dir = base_output_dir

            if not login:
                raise RuntimeError("Failed to load the login configuration")


            full_payload = self.__load_dictionary_data_or_file(key="payload", analysis=analysis, optional=True)
            config_data = self.__load_dictionary_data_or_file(key="config", analysis=analysis, optional=True)

            if not config_data and not full_payload:
                raise RuntimeError("Failed to load the config data")

            meta_data = self.__load_dictionary_data_or_file(key="meta", analysis=analysis, optional=True)
            data_cleaning = self.__load_dictionary_data_or_file(key="data_processing", analysis=analysis, optional=True)
            post_processing = self.__load_dictionary_data_or_file(key="post_processing", analysis=analysis, optional=True) 
            wait_for_results =str(analysis.get("wait_for_results", True)).lower() == "true"
            max_wait_in_seconds = int(analysis.get("max_wait_in_seconds", 600))

            self.add(
                login=login,
                input_file_path=analysis["file"],
                config_data=config_data,
                meta_data=meta_data,
                output_dir=output_dir,
                unzip_after_download=True,
                enabled=enabled,
                full_payload=full_payload,
                data_processing=data_cleaning,
                post_processing=post_processing,
                wait_for_results=wait_for_results,
                max_wait_in_seconds=max_wait_in_seconds
            )


    def __load_dictionary_data_or_file(self, key: str, analysis: Dict[str, Any], optional: bool = False ) -> Dict[str, Any] | None:
        data: Dict[str, Any] = {}
        data = analysis.get(key, {}).get("data", {})

        if data:
            return data

        file_path: str = analysis.get(key, {}).get("file")

        logger.info(
            {
                "message": f"Initializing {key} from file",
                "key": key,
                "file_path": file_path,
            }
        )
        if not file_path:
            if optional:
                return None
            raise RuntimeError(f"Data for {key} not found: {file_path}")
        
        path = FileUtility.load_filepath(file_path)
        if os.path.exists(path) is False:
            if optional:
                return None
            raise RuntimeError(f"Data for {key} not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    
