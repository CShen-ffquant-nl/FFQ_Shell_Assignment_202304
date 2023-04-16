from datetime import datetime
from .utilities.azure_blob_helper import BlobHelper
import json
from src.pricer.pricer_Black76 import Pricer_Black76
import logging

def upload_mkt_data(input: tuple[dict, str]) -> str:
    try:
        blob_helper = BlobHelper()
        run_id = input[1]

        for aPoint in input[0]:
            filename = aPoint["Time"]
            containerName = str(aPoint["Instrument"]).lower().replace(" ","-")
            data = aPoint["marketData"]
            blob_helper.upload(data, "marketdata", f"{containerName}/{filename}")

        return "Upload complete"
    except Exception as ex:
        logging.error(ex)
        return f"Exception: {ex}"


def upload_calib_data(input: tuple[dict, str]) -> str:
    try:
        
        blob_helper = BlobHelper()
        run_id = input[1]

        for aPoint in input[0]:
            filename = aPoint["Time"]
            containerName = str(aPoint["scenario"]).lower().replace(" ","-")
            data = aPoint["calibration"]
            blob_helper.upload(data, "calibrationdata",  f"{containerName}/{filename}")

        return "Upload complete"
    except Exception as ex:
        logging.error(ex)
        return f"Exception: {ex}"
    

def calculate_main(input: tuple[dict, str]) -> dict:
    try:
        
        blob_helper = BlobHelper()
        run_id = input[1]
        
        # prepare result
        output = input[0]
        
        for aContract in output:
            # upload input first
            filename = aContract["Time"]
            containerName = str(aContract["Contract"]).lower().replace(" ","-")
            contract_data = aContract["contractData"]
            blob_helper.upload(contract_data, "contractdata", f"{containerName}/{filename}")

            # download market data
            underlying_name= str(contract_data["Underlying"]).lower().replace(" ","-")
            filename=max(blob_helper.get_container("marketdata").list_blob_names(name_starts_with=underlying_name)) # choose the latest file name
            market_data = json.loads(blob_helper.download("marketdata" , filename).replace("\'", "\""))
            
            # download calibrationdata data
            scenario_name= str(contract_data["scenario"]).lower().replace(" ","-")
            filename=max(blob_helper.get_container("calibrationdata").list_blob_names(name_starts_with=scenario_name)) # choose the latest file name
            calib_data = json.loads(blob_helper.download("calibrationdata" , filename).replace("\'", "\""))
            
            #merge all 
            input=contract_data|market_data|calib_data
        
            # here is calculation
            model=Pricer_Black76(datetime.strptime(input["expire date"],"%Y-%m-%d"),input["Risk-Free Rate"]+input["dividend/carry on cost"],input["strike"])

            #NOTE: if the future price at expire date is not avaiable, exception will be thrown
            call,put =model.PV(datetime.strptime(input["pricing date"],"%Y-%m-%d"),input["future price"].get(input["expire date"]), input["Volatility"])

            aContract["market_data"]=market_data
            aContract["calibration_data"]=calib_data
            aContract["Call"] = call
            aContract["Put"]=put

        return output
    except Exception as ex:
        logging.error(ex)
        return f"Exception: {ex}"