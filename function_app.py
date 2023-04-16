"""
author: C.Shen

Azure durable function entrance (Azure fixed entrance name)

function_name (i.e. FFQ_Test2) is defined per Azure durable function
API name (i.e. upload_market_data) are function names decorated with "activity_trigger"

example:  https://ffqserver.azurewebsites.net/api/orchestrators/FFQ_Test2/upload_market_data

reference:
https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode?tabs=windows%2Cazure-cli-set-indexing-flag&pivots=python-mode-decorators
https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers?tabs=python    

"""
import azure.functions as func
import azure.durable_functions as df
import json
from src.main import calculate_main, upload_calib_data, upload_mkt_data
import logging


myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)
function_name = "FFQ_Test2"


"""
HTTP Trigger
"""


@myApp.route(route="orchestrators/" + function_name + "/{subFunctionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(req: func.HttpRequest, client: df.DurableOrchestrationClient) -> func.HttpResponse:
    # extract info from request
    sub_function_name = req.route_params.get("subFunctionName")
    payload = json.loads(req.get_body())

    # call ochestrator function by name, instanceID , pass in payload
    instance_id = await client.start_new("Orchestrator", None, (sub_function_name, payload))

    # create response
    response = client.create_check_status_response(req, instance_id)

    return response


"""
# Orchestrator
"""


@myApp.orchestration_trigger(context_name="context")
def Orchestrator(context: df.DurableOrchestrationContext):
    input = context.get_input()
    subFunctionName = input[0]
    payload = input[1]
    run_id = context.instance_id

    # basic pattern
    if not context.is_replaying:
        logging.info(f"Calling {subFunctionName}")

    result = yield context.call_activity(subFunctionName, (payload, run_id))
    return result


"""
# API: upload_market_data
"""


@myApp.activity_trigger(input_name="inputs")
def upload_market_data(inputs: tuple[dict, str]) -> str:
    logging.info(f"upload market data started")
    return upload_mkt_data(inputs)


"""
# API: upload_calibration_data
"""


@myApp.activity_trigger(input_name="inputs")
def upload_calibration_data(inputs: tuple[dict, str]):
    logging.info(f"upload calibration data started")
    return upload_calib_data(inputs)


"""
# API: upload_Contract and run
"""


@myApp.activity_trigger(input_name="inputs")
def upload_contract_and_run(inputs: tuple[dict, str]):
    logging.info(f"upload contract data and run started")
    return calculate_main(inputs)
