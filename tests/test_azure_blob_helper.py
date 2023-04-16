"""
Test class for src/utilities/azure_blob_helper.py

NOTE: An Azure storage account connection string is needed and hardcoded in the test.

"""

from src.utilities.azure_blob_helper import BlobHelper
from pytest import MonkeyPatch, fail
import pytest
import pandas as pd
import json

@pytest.fixture()
def init_blob(monkeypatch: MonkeyPatch):
    try:
        monkeypatch.setenv(
            "AzureWebJobsStorage", 
            "DefaultEndpointsProtocol=https;AccountName=ffqserver209276;AccountKey=WQyjLNF1F6LpOunrvDBf9CKW+naJUTuZ5XKbfM+uRwVE7k/h/OTPxnf0XlwsFLt/CRfJCFW5/oRo+AStpZri4w==;EndpointSuffix=core.windows.net")
       
        blob = BlobHelper()
        dummy_data= pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}).to_json()
        return blob,"20000101-test",dummy_data,"test-01"
       
    except Exception as e:
        fail(str(e))   
  

class TestAzureBlobHelper:
   
       
    def test_create_delete_container(self,init_blob: tuple[BlobHelper, str, str, str]):
        try:
            blob_helper=init_blob[0]
            container_2023 = blob_helper.get_container("20230101-test")
            assert container_2023.exists()

            blob_helper.delete_container("20230101-test")
            assert not container_2023.exists()

        except Exception as e:
            fail(str(e))

    def test_create_delete_blob(self,init_blob: tuple[BlobHelper, str, str, str]):
        try:
            blob_helper=init_blob[0]
            container_name=init_blob[1]

            blob_2023 = blob_helper.get_blob(container_name, "20230101-test")
            assert blob_2023.exists()

            blob_helper.delete_blob(container_name,"20230101-test")
            assert not blob_2023.exists()

        except Exception as e:
            fail(str(e))
   

    def test_blob_upload_download(self,init_blob: tuple[BlobHelper, str, str, str]):
        try:
            blob_helper=init_blob[0]
            container_name=init_blob[1]
            data=init_blob[2]
            file_name=init_blob[3]
            
            # test add blob
            assert blob_helper.upload(data,container_name,file_name)
            
            #test download blob
            data2=blob_helper.download(container_name,file_name)

            assert data2==json.dumps(data)

            # cleanup
            blob_helper.delete_blob(container_name,file_name)
            blob_helper.delete_container(container_name)

        except Exception as e:
            fail(str(e))