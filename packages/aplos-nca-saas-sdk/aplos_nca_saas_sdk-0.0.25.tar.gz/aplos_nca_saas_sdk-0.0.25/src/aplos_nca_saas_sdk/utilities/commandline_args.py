"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import argparse
import getpass
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from aplos_nca_saas_sdk.utilities.environment_vars import EnvironmentVars
from aplos_nca_saas_sdk.utilities.file_utility import FileUtility
# load the environment (.env) file if any
# this may or may not be the desired results
load_dotenv(override=True)


class CommandlineArgs:
    """Wrapper fro commandline args"""

    def __init__(self) -> None:
        # command line args
        self.parser = argparse.ArgumentParser(
            description="Example script to demonstrate command line argument parsing."
        )

        # Add the arguments
        self.parser.add_argument(
            "-u", "--username", required=False, help="The username"
        )
        self.parser.add_argument(
            "-p", "--password", required=False, help="The password"
        )
        self.parser.add_argument(
            "-c", "--config-file", required=False, help="Path to the configuration file"
        )
        self.parser.add_argument(
            "-f", "--analysis-file", required=False, help="Path to the analysis file"
        )
        self.parser.add_argument(
            "-m", "--metadata-file", required=False, help="Path to the metadata file"
        )

        self.parser.add_argument(
            "-d",
            "--host",
            required=False,
            help="The api host/host. Eg. api.aplos-nca.com, api.tenant.aplos-nca.com",
        )

        self.parser.add_argument(
            "-v", "--verbose", required=False, help="Detailed logging information"
        )

        self.parser.add_argument(
            "-s",
            "--skip",
            required=False,
            action="store_true",
            help="Skip prompts if required values have defaults",
        )
        self.parser.add_argument(
            "-o",
            "--output-directory",
            required=False,
            help="The full path to an output directory",
        )

        self.parser.add_argument(
            "-e",
            "--environment-file",
            required=False,
            help="The full path to an environment file (.env file).",
        )

        # auth information
        self.username: str | None = None
        self.password: str | None = None
        self.host: str | None = None

        # execution setup
        self.config_file: str | None = None
        self.config_file_default: str | None = None
        self.analysis_file: str | None = None
        self.analysis_file_default: str | None = None
        self.metadata_file: str | None = None
        self.metadata_file_default: str | None = None
        self.skip: bool = False
        self.output_directory: str | None = None
        self.output_directory_default: str = ".output"
        self.environment_file: str | None = None

        self.display_directions: bool = True

    def is_valid(self) -> bool:
        """
        Validates and Prompts the user if needed
        Returns:
            bool: True if they are all valid
        """
        # see if we have any arguments
        args = self.parser.parse_args()

        self.username = args.username
        self.password = args.password
        self.config_file = args.config_file
        # anything with a dash (in the args) is accessed with an underscore
        self.analysis_file = args.analysis_file
        self.host = args.host

        self.metadata_file = args.metadata_file
        self.skip = args.skip
        self.output_directory = args.output_directory
        self.environment_file = args.environment_file
        # no args check to see if they have them in the environment

        # if we have an environment file we'll want to load it before checking any defaults
        self.check_for_environment_config()

        env = EnvironmentVars()

        if not self.username:
            if self.skip and env.username:
                self.username = env.username
            else:
                self.username = self.prompt_for_input("username", env.username)
        if not self.password:
            if self.skip and env.password:
                self.password = env.password
            else:
                self.password = self.prompt_for_input(
                    "password", env.password, is_sensitive=True
                )

        if not self.host:
            if self.skip and env.host:
                self.host = env.host
            else:
                self.host = self.prompt_for_input("Api Domain", env.host)

        if not self.analysis_file:
            if self.skip and self.analysis_file_default or env.analysis_file:
                self.analysis_file = self.analysis_file_default or env.analysis_file
            else:
                self.analysis_file = self.prompt_for_input(
                    "Analysis File", self.analysis_file_default or env.analysis_file
                )

        if not self.config_file:
            if self.skip and self.config_file_default or env.config_file:
                self.config_file = self.config_file_default or env.config_file
            else:
                self.config_file = self.prompt_for_input(
                    "Configuration File", self.config_file_default or env.config_file
                )

        if not self.metadata_file:
            if self.skip and self.metadata_file_default or env.metadata_file:
                self.metadata_file = self.metadata_file_default or env.metadata_file
            else:
                self.metadata_file = self.prompt_for_input(
                    "MetaData File",
                    self.metadata_file_default or env.metadata_file,
                    required=False,
                )
        if not self.output_directory:
            if self.skip:
                self.output_directory = self.output_directory_default
            else:
                self.output_directory = self.prompt_for_input(
                    "Output directory (the full path)",
                    self.output_directory_default,
                    required=False,
                )

        # do we have everything we need?

        return self.__check_all_required()

    def __check_all_required(self) -> bool:
        """
        Check to see if all the fields are required
        Returns:
            bool: True if all required fields are populated, otherwise false
        """
        # basically everything except metadata
        required_fields = [
            self.username,
            self.password,
            self.analysis_file,
            self.config_file,
            self.host,
        ]
        for field in required_fields:
            if not field:
                return False

        return True

    def prompt_for_input(
        self,
        prompt: str,
        default: str | None = None,
        is_sensitive: bool = False,
        required: bool = True,
    ) -> str | None:
        """
        Create a prompt to display
        Args:
            prompt (str): The Prompt
            default (str | None, optional): Default Value. Defaults to None.
            is_sensitive (bool, optional): If the data is sensitive it won't be displayed on the screen. Defaults to False.
            required (bool, optional): If the field is required. Defaults to True.

        Returns:
            str | None: The result of the prompt
        """
        # Construct the prompt message to include the default option if provided
        if self.display_directions:
            self.display_directions = False
            print("Hit enter if you wish to accept a default value (if available)")
            print("")
        default_display = default if not is_sensitive else "************"
        required_display = " - Required" if required else " - Optional"

        display = (
            f" [{default_display}]: "
            if default
            else f" [No Default{required_display}]: "
        )
        user_input: str | None = None
        if is_sensitive:
            user_input = getpass.getpass(f"{prompt}{display}")
        else:
            prompt_message = f"{prompt}{display}"

            # Get user input
            user_input = input(prompt_message)

        # Return the user input if not empty, otherwise return the default value
        user_input = user_input if user_input else default

        if not user_input and required:
            return self.prompt_for_input(
                prompt=prompt,
                default=default,
                is_sensitive=is_sensitive,
                required=required,
            )

        return user_input

   

    def check_for_environment_config(self):
        """Attempts to load an environment file"""
        if not self.environment_file:
            return  # Exit early if no environment file is provided

        env_file_path = Path(self.environment_file)

        if not env_file_path.exists():
            # Try to find the file
            fu: FileUtility = FileUtility()
            file = fu.find_file(__file__, env_file_path.name)
            file_path = Path(str(file))

            if not file_path.exists():
                print("\n\nAn environment file was provided but it doesn't exist.")
                print(f"\tFile provided: {self.environment_file}")
                exit()
            else:
                self.environment_file = str(file_path)

        load_dotenv(dotenv_path=self.environment_file, override=True)


def main():
    args = CommandlineArgs()

    if args.is_valid():
        pwd = "************" if args.password else "empty"
        print(f"username = {args.username}")
        print(f"password = {pwd}")

        print(f"host = {args.host}")
        print(f"analysis_file = {args.analysis_file}")

        print(f"config_file = {args.config_file}")
        print(f"metadata_file = {args.metadata_file}")

        print(f"output_directory = {args.output_directory}")

        print("✅ All required parameters are accounted for.")

    else:
        print("Missing some required fields.")


if __name__ == "__main__":
    main()
