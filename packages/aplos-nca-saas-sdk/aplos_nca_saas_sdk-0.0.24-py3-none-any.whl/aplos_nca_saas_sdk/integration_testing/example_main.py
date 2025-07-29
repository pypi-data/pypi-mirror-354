"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from pathlib import Path
from aplos_nca_saas_sdk.utilities.environment_services import EnvironmentServices
from aplos_nca_saas_sdk.integration_testing.integration_test_suite import (
    IntegrationTestSuite,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)


def main():
    """This is an example on how you can run the unit tests"""

    # Optionally use our convenient Environment Services loader
    # which can help during initial testings.
    evs: EnvironmentServices = EnvironmentServices()
    # see if we have a local .env, .env.uat, etc configured to look up
    env_file = os.getenv("ENV_FILE")
    if env_file:
        # if we have an environment file defined, let's load it
        evs.load_environment(starting_path=__file__, file_name=env_file)

    # this is where the work begins
    its: IntegrationTestSuite = IntegrationTestSuite()
    config: TestConfiguration = TestConfiguration()

    # here were going to load a config file that is local, for security purpose
    # you should store this in SecretsManager, Parameter Store, a secure S3 bucket etc.
    # the configs typically contain sensitive information like usernames & passwords
    # so be careful where you store it!
    config_file = os.path.join(
        Path(__file__).parent,
        "configs",
        os.getenv("TEST_CONFIG_FILE") or "config_sample.json",
    )
    # load it so we can see what it looks like
    config.load(file_path=config_file)

    # run the tests
    its.test(test_config=config)


def override_config(config: TestConfiguration):
    """
    Override the configuration for the tests.
    This is some sample code how you can use a combination of a config file
    and then override the username/password combos using environment vars.
    """
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")
    host = os.getenv("TEST_HOST")

    if not username or not password or not host:
        raise RuntimeError(
            "TEST_USERNAME, TEST_PASSWORD, and TEST_HOST must be set in the environment"
        )

    config.logins.list.clear()
    config.logins.add(username=username, password=password, host=host)

    config.app_config.hosts.list.clear()
    config.app_config.hosts.add(host=host)


if __name__ == "__main__":
    main()
