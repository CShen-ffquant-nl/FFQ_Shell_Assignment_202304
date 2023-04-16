"""
Helper class for handling Azure storage 

ref: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
ref: https://learn.microsoft.com/en-us/python/api/azure-storage-blob/?view=azure-python

"""

import os
import uuid
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient, BlobType
import json
import logging


class BlobHelper:
    def __init__(self) -> None:
        try:
            # Retrieve the connection string from local.setting.json or Application Settings
            self.conn_string = os.environ["AzureWebJobsStorage"]

            # Create the blob service client
            self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_string)
        # list all the container names

        except Exception as ex:
            print(f"Exception: {ex}")
            logging.error(ex)
            raise Exception(ex)

    """
    get container by name. If not exist, create one 
    """

    def get_container(self, name: str = None) -> ContainerClient:
        try:
            # Create a unique name for the container
            if name == None:
                name = str(uuid.uuid4())

            container_client = self.blob_service_client.get_container_client(name)
            if not container_client.exists():
                self.blob_service_client.create_container(name)

            return container_client

        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return None

    """
    get blob by name. If either blob or container is not exist, create one 
    """

    def get_blob(self, container_name: str, file_name: str) -> BlobClient:
        try:
            blob_client = self.blob_service_client.get_blob_client(container_name, file_name)
            if not blob_client.exists():
                # makesure container exists
                self.get_container(container_name)
                # create a new blob
                blob_client.create_append_blob()
                # rename the blob
                blob_client.blob_name = file_name
                return BlobClient.from_connection_string(self.conn_string, container_name, file_name)

            return blob_client

        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return None

    """
    delete container by name. also including blob inside
    """

    def delete_container(self, container_name: str = None) -> bool:
        try:
            container_client = self.get_container(container_name)
            # delete self
            container_client.delete_container()
            return True
        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return False

    """
    delete blob by name
    """

    def delete_blob(self, container_name: str, file_name: str):
        try:
            blob_client = self.get_blob(container_name, file_name)
            # delete self
            blob_client.delete_blob()
            return True
        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return False

    """
    upload data to a blob. create container and blob if not exist
    """

    def upload(self, data: str, container_name: str, file_name: str, overwrite_flag: bool = True):
        try:
            blob_client = self.get_blob(container_name, file_name)
            # extra convertion to string
            blob_client.upload_blob(json.dumps(data), blob_type=BlobType.APPENDBLOB, overwrite=overwrite_flag)
            return True
        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return False

    """
    download data to a blob. create empty container and blob if not exist
    """

    def download(self, container_name: str, file_name: str) -> str:
        try:
            blob_client = self.get_blob(container_name, file_name)

            # encoding param is necessary for readall() to return str, otherwise it returns bytes
            downloader = blob_client.download_blob(max_concurrency=1, encoding="UTF-8")
            data = downloader.readall()

            return data
        except Exception as ex:
            print(f"Exception {ex}")
            logging.error(ex)
            return None
