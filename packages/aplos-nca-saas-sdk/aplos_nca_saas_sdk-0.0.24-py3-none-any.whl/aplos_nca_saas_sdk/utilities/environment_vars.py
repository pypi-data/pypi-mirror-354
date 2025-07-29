"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os


class EnvironmentVars:
    """Loading Environment Vars or replace them with runtime values"""

    def __init__(self) -> None:
        # load defaults
        self.host = os.getenv("APLOS_host", "")

        self.aws_region = os.getenv("COGNITO_REGION")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.username = os.getenv("COGNITO_USER_NAME")
        self.password = os.getenv("COGNITO_PASSWORD")

        self.config_file = os.getenv("CONFIG_FILE")
        self.metadata_file = os.getenv("METADATA_FILE")
        self.analysis_file = os.getenv("ANALYSIS_FILE")

        if self.host is not None and "https://" in self.host:
            self.host = self.host.replace("https://", "")

        self.aplos_api_url = f"https://{self.host}"

    @staticmethod
    def is_running_in_aws_lambda():
        """
        A quick way to check if we are running in an AWS Lambda Environment
        """
        return "AWS_LAMBDA_FUNCTION_NAME" in os.environ
