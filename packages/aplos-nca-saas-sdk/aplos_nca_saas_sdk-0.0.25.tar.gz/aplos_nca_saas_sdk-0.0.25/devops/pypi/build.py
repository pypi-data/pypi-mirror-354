import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import List

import toml
from aws_lambda_powertools import Logger

logger = Logger()


def main():
    """build the artifacts"""
    project_root = Path(__file__).parents[2]

    # extract the version
    pyproject_toml = os.path.join(project_root, "pyproject.toml")
    version_file = os.path.join(project_root, "src", "aplos_nca_saas_sdk", "version.py")

    if not os.path.exists(pyproject_toml):
        raise FileNotFoundError(
            f"The pyproject.toml file ({pyproject_toml}) not found. "
            "Please check the path and try again."
        )

    extract_version_and_write_to_file(pyproject_toml, version_file)
    # do the build
    run_local_clean_up()

    run_build()
    run_publish()


def run_local_clean_up():
    """run a local clean up and remove older items in the dist directory"""
    project_root = Path(__file__).parents[2]
    dist_dir = os.path.join(project_root, "dist")
    if os.path.exists(dist_dir):
        # clear it out
        shutil.rmtree(dist_dir)


def run_remote_clean_up():
    """
    Clean out older versions
    """
    logger.warning("warning/info: older versions are not being cleaned out.")


def extract_version_and_write_to_file(pyproject_toml: str, version_file: str):
    """
    extract the version number from the pyproject.toml file and write it
    to the version.py file
    """
    if not os.path.exists(pyproject_toml):
        raise FileNotFoundError(
            f"The pyproject.toml file ({pyproject_toml}) not found. "
            "Please check the path and try again."
        )

    with open(pyproject_toml, "r", encoding="utf-8") as file:
        pyproject_data = toml.load(file)
        version = pyproject_data["project"]["version"]
        with open(version_file, "w", encoding="utf-8") as f:
            f.write("# Aplos NCA SaaS SDK Version File\n")
            f.write("# This is automatically generated during the build process. \n")
            f.write("# DO NOT UPDATE IT DIRECTLY. IT WILL BE OVERWRITTEN. \n")
            f.write(f"__version__ = '{version}'\n")


def run_build():
    """Run python build commands"""
    output = run_commands(["python", "-m", "build"], capture_output=True)


def run_publish():
    """publish to code artifact"""

    # Set up the environment variables for the upload command
    api_token = os.getenv("PYPI_API_TOKEN")

    if not api_token:
        raise ValueError("PYPI_API_TOKEN environment variable is not set.")

    env = os.environ.copy()
    env["TWINE_USERNAME"] = "__token__"
    env["TWINE_PASSWORD"] = api_token

    run_commands(
        ["python", "-m", "twine", "upload", "dist/*"],
        env=env,
    )


def get_url(payload: str):
    """get the url from the payload"""
    value: dict = json.loads(payload)
    url = value.get("repositoryEndpoint")

    return url


def run_commands(
    commands: List[str], capture_output: bool = False, env=None
) -> str | int | None:
    """centralized area for running process commands"""
    try:
        # Run the publish command
        result = subprocess.run(
            commands,
            check=True,
            capture_output=capture_output,
            env=env,  # pass any environment vars
            # capture errors
            stderr=subprocess.PIPE if not capture_output else None,
            # capture output
            stdout=subprocess.PIPE if not capture_output else None,
            text=True,
        )

        # if capture_output:
        output = str(result.stdout)
        print(output)
        return output

    except subprocess.CalledProcessError as e:
        logger.exception(f"An error occurred: {e}")
        if e.stderr:
            error = str(e.stderr)
            if "401 Error" in error:
                logger.error("401 Error: Invalid credentials")
                if "amazonaws" in error:
                    logger.error(
                        "Please check your AWS credentials and try again."
                    )
                    print("🚨 If you this package doesn't use aws code artifact, check your pip config file "
                          "and remove the aws code artifact reference "
                          "mac: ~./.config/pip/pip.conf"
                          )
                else:
                    logger.error(
                        "Please check your PYPI_API_TOKEN environment variable."
                    )   
                
                logger.error("If you need help, please contact support.")
        return e.returncode

if __name__ == "__main__":
    main()
