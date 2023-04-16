'''
Test class for src/main.py

'''

from src.main import calculate_main, upload_calib_data, upload_mkt_data
from src.utilities.azure_blob_helper import BlobHelper
from pytest import MonkeyPatch, fail
import pytest
import json
from pathlib import Path


@pytest.fixture()
def init_blob(monkeypatch: MonkeyPatch):
    try:
        monkeypatch.setenv(
            "AzureWebJobsStorage",
            "DefaultEndpointsProtocol=https;AccountName=ffqserver209276;AccountKey=WQyjLNF1F6LpOunrvDBf9CKW+naJUTuZ5XKbfM+uRwVE7k/h/OTPxnf0XlwsFLt/CRfJCFW5/oRo+AStpZri4w==;EndpointSuffix=core.windows.net",
        )

        with open(
            Path.joinpath(Path.cwd(), "tests", "dummy_input_market.json")
        ) as file:
            dummy_input_market = json.load(file)

        with open(
            Path.joinpath(Path.cwd(), "tests", "dummy_input_contract.json")
        ) as file:
            dummy_input_contract = json.load(file)

        with open(Path.joinpath(Path.cwd(), "tests", "dummy_input_calib.json")) as file:
            dummy_input_calib = json.load(file)

        with open(Path.joinpath(Path.cwd(), "tests", "dummy_output.json")) as file2:
            dummy_output = json.load(file2)

        run_id = "123456789"
        return (
            dummy_input_market,
            dummy_input_calib,
            dummy_input_contract,
            dummy_output,
            run_id,
        )

    except Exception as e:
        fail(str(e))


class Test_Main:
    def test_market_data(self, init_blob: tuple):
        try:
            input = init_blob[0]
            run_id = init_blob[-1]
            blob_helper = BlobHelper()

            # upload
            result = upload_mkt_data((input, run_id))
            assert result == "Upload complete"

            for aData in input:
                containerName = str(aData["Instrument"]).lower().replace(" ", "-")
                filename = aData["Time"]

                # download check
                market_data = json.loads(
                    blob_helper.download(
                        f"marketdata", f"{containerName}/{filename}"
                    ).replace("'", '"')
                )
                assert market_data == aData["marketData"]

                # cleanup
                blob_helper.delete_blob(f"marketdata", f"{containerName}/{filename}")

        except Exception as e:
            fail(str(e))

    def test_calib_data(self, init_blob: tuple[str, str]):
        try:
            input = init_blob[1]
            run_id = init_blob[-1]
            blob_helper = BlobHelper()

            # upload
            result = upload_calib_data((input, run_id))
            assert result == "Upload complete"

            for aData in input:
                containerName = str(aData["scenario"]).lower().replace(" ", "-")
                filename = aData["Time"]

                # download check
                market_data = json.loads(
                    blob_helper.download(
                        f"calibrationdata", f"{containerName}/{filename}"
                    ).replace("'", '"')
                )

                assert market_data == aData["calibration"]

                # cleanup
                blob_helper.delete_blob(f"calibrationdata", f"{containerName}/{filename}")

        except Exception as e:
            fail(str(e))

    def test_main(self, init_blob: tuple[str, str]):
        try:
            # init
            blob_helper = BlobHelper()
            run_id = init_blob[-1]
            upload_mkt_data((init_blob[0], run_id))
            upload_calib_data((init_blob[1], run_id))
            input = init_blob[2]

            # upload and calculate
            result = calculate_main((input, run_id))
            assert init_blob[3][1]["Call"] == result[1]["Call"]

            # check
            for aData in input:
                containerName = str(aData["Contract"]).lower().replace(" ", "-")
                filename = aData["Time"]

                # download check
                contract_data = json.loads(
                    blob_helper.download(
                        f"contractdata", f"{containerName}/{filename}"
                    ).replace("'", '"')
                )

                assert contract_data == aData["contractData"]

            # cleanup data
            for aData in init_blob[2]:
                containerName = str(aData["Contract"]).lower().replace(" ", "-")
                filename = aData["Time"]
                blob_helper.delete_blob(f"contractdata", f"{containerName}/{filename}")

            for aData in init_blob[1]:
                containerName = str(aData["scenario"]).lower().replace(" ", "-")
                filename = aData["Time"]
                blob_helper.delete_blob(f"calibrationdata", f"{containerName}/{filename}")

            for aData in init_blob[0]:
                containerName = str(aData["Instrument"]).lower().replace(" ", "-")
                filename = aData["Time"]
                blob_helper.delete_blob(f"marketdata", f"{containerName}/{filename}")
        except Exception as e:
            fail(str(e))
