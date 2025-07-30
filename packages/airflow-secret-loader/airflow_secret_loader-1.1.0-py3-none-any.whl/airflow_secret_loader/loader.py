
import os
import json
import boto3
import logging
from azure.identity import ManagedIdentityCredential
from airflow.exceptions import AirflowException

def assume_role_with_azure_identity(role_arn, managed_identity_client_id, azure_application_id, session_name):
    logging.info('Requesting Azure AD token')
    azure_identity = ManagedIdentityCredential(client_id=managed_identity_client_id)
    azure_token = azure_identity.get_token(azure_application_id)
    logging.info('Assuming AWS role')
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role_with_web_identity(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        WebIdentityToken=azure_token.token
    )
    logging.info(f'credentials received expiry {str(assumed_role["Credentials"]["Expiration"])}')
    return assumed_role['Credentials']

def get_aws_secrets():
    role_arn = os.getenv("SECRET_ROLE_ARN")
    secret_id = os.getenv("SECRET_ID")
    managed_identity_client_id = os.getenv("MANAGED_IDENTITY_CLIENT_ID")
    azure_application_id = os.getenv("AZURE_APPLICATION_ID")

    if not role_arn or not secret_id:
        raise AirflowException("SECRET_ROLE_ARN or SECRET_ID not set")

    use_azure = os.getenv("USE_AZURE_IDENTITY", "false").lower() == "true"

    if use_azure:
        creds = assume_role_with_azure_identity(role_arn, managed_identity_client_id, azure_application_id, "AzFuncSession")
    else:
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
        return json.loads(secret_string)
    except json.JSONDecodeError:
        return {"raw_secret": secret_string}
