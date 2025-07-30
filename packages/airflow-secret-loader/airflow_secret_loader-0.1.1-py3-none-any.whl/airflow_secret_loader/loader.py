
import os
import json
import boto3
from airflow.exceptions import AirflowException

def load_env_from_aws_secret():
    role_arn = os.getenv("SECRET_ROLE_ARN")
    secret_id = os.getenv("SECRET_ID")

    if not role_arn or not secret_id:
        raise AirflowException("SECRET_ROLE_ARN or SECRET_ID not set")

    sts = boto3.client("sts")
    assumed = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AirflowSecretSession"
    )

    creds = assumed["Credentials"]
    session = boto3.session.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"]
    )

    secrets_client = session.client("secretsmanager")
    response = secrets_client.get_secret_value(SecretId=secret_id)
    secret_string = response.get("SecretString")

    try:
        secret_dict = json.loads(secret_string)
        for k, v in secret_dict.items():
            os.environ[f"AIRFLOW_VAR_{k.upper()}"] = v
    except json.JSONDecodeError:
        os.environ["AIRFLOW_VAR_MY_SECRET"] = secret_string
