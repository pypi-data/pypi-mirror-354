# Integration Test

This module runs integration tests against a live environment.  The goal is to catch anything before it's deployed.
However you can also use this as a learning tool or a base on how to use our API's.

## Requirements
The integration tests will require the following:
- A valid user Aplos NCA User Account
- A valid subscription


### Users
You will need valid user accounts with the appropriate permissions for the endpoints they are executing.

If you are testing permission boundaries then you should set up multiple users with different permissions.


### Subscriptions
Your subscription will control how may executions are allowed for user or tenancy.  Make sure you have enough executions.  If you need
additional executions, please reach-out to your support contact.

## Running the test
See the `example_main.py` for updated examples, but in general you follow the code below to run tests.  Also, see the `configs` section below
for guidance on defining what is tested.

```python
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
    # See if we have a local .env, .env.uat, etc configured to look up
    # for local configuration settings
    # 
    # Use local .env files when testing locally.  As a best practice
    # you should avoid adding these to source control or deployments.
    env_file = os.getenv("ENV_FILE")
    if env_file:
        # if we have an environment file defined, let's load it
        # this will prep our environment with local values.
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


```

### Configs
Tests are run based on configurations.  The following is an example of supported configurations:

- Application Configuration Settings
- Logins & Access
- Executing an Analysis
- Running a Validation

```json
{
    "application_config_test": {
        "purpose": "Tests the application configuration endpoints",
        "hosts": [
            {
                "host": "api.example.com",
                "expected_results": {
                    "status_code": 200
                },
                "enabled": true
            },
            {
                "host": "XXXXXXXXXXXXXXXXXXXXX",
                "expected_results": {
                    "status_code": 403
                },
                "enabled": false
            }
        ]
    },
    "login_test": {
        "purpose": "Tests the login endpoints",
        "logins": [
            {
                "username": "foo",
                "password": "barr",
                "host": "api.example.com",
                "roles": []
            },
            {
                "username": "XXXXXXXXXXXXXXXXXXXXX",
                "password": "XXXXXXXXXXXXXXXXXXXXX",
                "host": "XXXXXXXXXXXXXXXXXXXXX",
                "roles": [
                    "XXXXXXXXXXXXXXXXXXXXX"
                ],
                "enabled": false,
                "expected_results": {
                    "exception": "InvalidCredentialsException"
                }
            }
        ]
    },
    "file_upload_test": {
        "purpose": "Tests the file upload endpoints.",
        "notes": "a file can be on the local drive or pulled from a public https source.",
        "login": {
            "purpose": "optional: if present this login is used, unless a specific login is defined for the test",
            "username": "foo",
            "password": "bar",
            "host": "api.example.com"
        },
        "files": [
            {
                "file": "XXXXXXXXXXXXXXXXXXXXX"
            },
            {
                "file": "XXXXXXXXXXXXXXXXXXXXX",
                "login": {
                    "purpose": "optional: if present tests an upload for a specific user",
                    "username": "XXXXXXXXXXXXXXXXXXXXX",
                    "password": "XXXXXXXXXXXXXXXXXXXXX",
                    "host": "XXXXXXXXXXXXXXXXXXXXX"
                }
            }
        ]
    },
    "analysis_execution_test": {
        "purpose": "Tests the analysis execution endpoints.",
        "login": {
            "username": "XXXXXXXXXXXXXXXXXXXXX",
            "password": "XXXXXXXXXXXXXXXXXXXXX",
            "host": "XXXXXXXXXXXXXXXXXXXXX"
        },
        "output_dir": "XXXXXXXXXXXXXXXXXXXXX",
        "analyses": [
            {
                "file": "XXXXXXXXXXXXXXXXXXXXX",
                "meta": {},
                "config": {},
                "expected_results": {
                    "status_code": 200
                },
                "output_dir": "XXXXXXXXXXXXXXXXXXXXX"
            },
            {
                "file": "XXXXXXXXXXXXXXXXXXXXX",
                "meta": {},
                "config": {},
                "login": {
                    "username": "XXXXXXXXXXXXXXXXXXXXX",
                    "password": "XXXXXXXXXXXXXXXXXXXXX",
                    "host": "XXXXXXXXXXXXXXXXXXXXX"
                },
                "expected_results": {
                    "status_code": 200
                }
            }
        ]
    },
    "validation_test": {
        "purpose": "Tests the validation execution.",
        "login": {
            "username": "XXXXXXXXXXXXXXXXXXXXX",
            "password": "XXXXXXXXXXXXXXXXXXXXX",
            "host": "XXXXXXXXXXXXXXXXXXXXX"
        },
        "expected_results": {
            "status_code": 200
        }
    }
}

```