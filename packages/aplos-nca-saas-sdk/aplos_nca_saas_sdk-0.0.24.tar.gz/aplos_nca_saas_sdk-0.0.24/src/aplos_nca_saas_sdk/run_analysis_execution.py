"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
import os
from pathlib import Path

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.nca_resources.nca_analysis import NCAAnalysis
from aplos_nca_saas_sdk.utilities.commandline_args import CommandlineArgs

logger = Logger()


def main():
    """Run Main when then file is run directly"""
    try:
        print("Welcome to the NCA Engine Upload & Execution Demo")
        args = CommandlineArgs()
        files_path = os.path.join(
            Path(__file__).parent, "sample_files", "analysis_files", "single_ev"
        )

        # set up some defaults to make the demos quicker
        args.analysis_file_default = os.path.join(files_path, "input.csv")
        args.config_file_default = os.path.join(files_path, "config.json")
        args.metadata_file_default = os.path.join(files_path, "meta_data.json")
        args.output_directory_default = os.path.join(files_path, ".output")
        if not args.is_valid():
            print("\n\n")
            print("Missing some arguments.")
            exit()

        analysis_api = NCAAnalysis(host=str(args.host))
        analysis_api.verbose = True

        print("\tLoading analysis configurations")
        print(f"\t\t...{os.path.basename(args.config_file)}")
        config_data: dict = read_json_file(str(args.config_file))

        print("\tLoading analysis meta data")
        print(f"\t\t...{os.path.basename(args.metadata_file)}")
        meta_data = optional_json_loads(read_text_file(str(args.metadata_file)))

        wait_for_results = True
        max_wait_in_seconds = 900  # 15 minutes
        results = analysis_api.execute(
            username=str(args.username),
            password=str(args.password),
            input_file_path=str(args.analysis_file),
            config_data=config_data,
            meta_data=meta_data,
            output_directory=str(args.output_directory),
            wait_for_results=wait_for_results,
            max_wait_in_seconds=max_wait_in_seconds,
        )

        if not wait_for_results:
            exec_id = results.get("execution", {}).get("execution_id", "")
            print(
                "Analysis execution has been queued.  We're not waiting for the results."
            )
            print(f"Please check your results with execution id {exec_id}.")

        print("🙌 Thank you for using the NCA API for an Analysis Execution Demo. 🙌")
    except Exception as e:  # pylint: disable=w0718
        print(
            "🚨 An error occurred ... exiting with an error.  Please check your settings and try again."
        )
        print(
            "If you believe this is bug please create a support ticket and include the execution id (if available)."
        )
        print(
            "If it's not reported in the error below check your account for the failed execution."
        )

        print(str(e))


def optional_json_loads(data: str | dict) -> str | dict:
    """
    Attempts to load the data as json, fails graceful and returns the data is if it fails
    Args:
        data (str): data as string

    Returns:
        str | dict: either the data as is or a converted dictionary/json object
    """
    if isinstance(data, dict):
        return data

    try:
        data = json.loads(str(data))
    finally:
        pass
    return data


def read_json_file(file_path: str) -> dict:
    """
    Reads a file and returns the json
    Args:
        file_path (str): _description_

    Raises:
        FileNotFoundError: _description_

    Returns:
        dict: _description_
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File Not Found: {file_path}")

    data = None
    with open(file_path, mode="r", encoding="utf8") as file:
        data = json.load(file)

    return data


def read_text_file(file_path: str) -> str:
    """
    Read files contents
    Args:
        file_path (str): path to the file

    Raises:
        FileNotFoundError: if the file is not found

    Returns:
        str: the files data
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File Not Found: {file_path}")

    data = None
    with open(file_path, mode="r", encoding="utf8") as file:
        data = file.read()

    return data


if __name__ == "__main__":
    main()
