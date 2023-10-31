import boto3

SSM_CLIENT = boto3.client("ssm")
REGION_NAME = "us-west-2"


def get_unencrypted_parameter(name: str) -> str:
    return SSM_CLIENT.get_parameter(Name=name, WithDecryption=False)("Parameter")[
        "Value"
    ]


def get_encrypted_parameter(name: str) -> str:
    return SSM_CLIENT.get_parameter(Name=name, WithDecryption=True)("Parameter")[
        "Value"
    ]
