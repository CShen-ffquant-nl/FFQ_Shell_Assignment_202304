"""
author: C.Shen

function entrance (Azure fixed entrance name)
reference:
https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode?tabs=windows%2Cazure-cli-set-indexing-flag&pivots=python-mode-decorators

https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers?tabs=python    

"""

import azure.functions as func
import azure.durable_functions as df
import json
from src.main import calculate_main, upload_calib_data, upload_mkt_data
import logging

# =================
# Only change function name here unless necessary
# example:  https://ffqserver.azurewebsites.net/api/orchestrators/FFQ_Test2/run
function_name = "FFQ_Test2"
# ================


myApp = df.DFApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# ==============#
# An HTTP-Triggered Function with a Durable Functions Client binding
# only route with the same function_name will be triggered.
@myApp.route(route="orchestrators/" + function_name + "/{subFunctionName}")
@myApp.durable_client_input(client_name="client")
async def http_start(
    req: func.HttpRequest, client: df.DurableOrchestrationClient
) -> func.HttpResponse:
    # route paramter deined in route() decorator

    sub_function_name = req.route_params.get("subFunctionName")
    payload = json.loads(req.get_body())

    # client object is initialized in decorator and passed in this function
    # ochestrator function name, instanceID , payload
    instance_id = await client.start_new(
        "Orchestrator", None, (sub_function_name, payload)
    )
    # create response
    response = client.create_check_status_response(req, instance_id)
    return response


# ==============#
# Orchestrator function
# for now, it's fixed to Orchestrator as we expect one orchestrator per durable function instance
@myApp.orchestration_trigger(context_name="context")
def Orchestrator(context: df.DurableOrchestrationContext):
    # NOTE: if directly calling engine_main(), process's state information may be lost
    # call_activity() returns wrapped task with action and information

    input = context.get_input()
    subFunctionName = input[0]
    payload = input[1]
    run_id = context.instance_id

    # basic pattern
    if not context.is_replaying:
        logging.info(f"Calling {subFunctionName}")

    result = yield context.call_activity(subFunctionName, (payload, run_id))
    return result


# # ==============#
# @myApp.activity_trigger(input_name="inputs")
# def return_id2(inputs: str) -> str:
#     return inputs


# @myApp.activity_trigger(input_name="inputs")
# def return_id(inputs: tuple[dict, str]) -> str:
#     return inputs[1]


# ==============#
# API: upload_market_data
@myApp.activity_trigger(input_name="inputs")
def upload_market_data(inputs: tuple[dict, str]) -> str:

    logging.info(f"upload market data started")
    return upload_mkt_data(inputs)


# ==============#
# API: upload_calibration_data
@myApp.activity_trigger(input_name="inputs")
def upload_calibration_data(inputs: tuple[dict, str]):
    
    logging.info(f"upload calibration data started")
    return upload_calib_data(inputs)


# ==============#
# API: upload_Contract and run
@myApp.activity_trigger(input_name="inputs")
def upload_contract_and_run(inputs: tuple[dict, str]):

    logging.info(f"upload contract data and run started")
    return calculate_main(inputs)
