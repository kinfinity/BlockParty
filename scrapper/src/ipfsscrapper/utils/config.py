import json
import logging
from pathlib import Path, PurePath
from typing import Any

import boto3
from botocore.exceptions import ClientError

from ipfsscrapper.utils import json_fp


def get_secret(secret_name, region_name="us-east-2") -> Any:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError:
        logging.exception("Failed to get secret '%s'", secret_name)
        raise
    else:
        json_secret = json.loads(get_secret_value_response["SecretString"])
    return json_secret


class Config:
    def __init__(self, config_path: PurePath):
        config_file = json_fp.load_json(config_path)
        self.db_host = config_file["db_host"]
        self.db_port = config_file["db_port"]
        self.database = config_file["database"]
        self.db_username = config_file["db_username"]
        self.db_password = config_file["db_password"]
        self.AWS_ID = config_file["AWS_ID"]
        self.AWS_KEY = config_file["AWS_KEY"]
        self.ipfs_cids = config_file["ipfs_cids"]
        self.ipfs_url = config_file["ipfs_url"]
        self.batch_number = config_file["batch_number"]
