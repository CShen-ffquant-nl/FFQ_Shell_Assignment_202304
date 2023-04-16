# Shell Assignment 2023-04-14 

========================

## Assignment: Implement a REST API web application for option pricing and market data storage 

(recommended timing: 2-3 hours) 

 

## Features: 

Upload market data required for option pricing 

Retrieve previously uploaded market data 

Calculate PV of options with Black76 formula using previously uploaded market data 

  

## Examples of options: 

BRN Jan24 Call Strike 100 USD/BBL 

HH Mar24 Put Strike 10 USD/MMBTu 

  

A note on the contract notation. A BRN Jan-24 option is a European option with underlying ICE Brent Jan-24 Future. BRN option expiry will be the last business day of the 2nd month before the delivery month. For example, BRN Jan-24 expiry date is 2023-11-30. 

HH Mar24 option is a European option with underlying Henry Hub Gas March 24 Future contract. HH option expiry is the last business day of the month before the delivery month. For example, HH Mar-24 expiry date is 2022-02-29. 

 

You have a freedom to choose technology stack, architecture, input/output schemas to best fit the requirements. 

  

The code and design should meet these requirements, but be sufficiently flexible to allow future changes. The code should be well structured, commented, have error handling and be tested. 

 

Produce working, object-oriented source code. 

Provide as a GitHub project or send back in electronic format. 

We will walk through your code together in the next session, answering questions on the code and programming/design choices you made. 

At the interview you will be asked to present an end-to-end demo of the application. 

==================================

# API

## upload market data

### Purpose

Upload and save (realworld) underlying market data in Azure storage. They can come from internal/external market data provider. 

### Address:

[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_market_data](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_market_data)

### Body example:

```json

[
  {
    "Instrument": "ICE Brent Jan-24 Future",
    "Time": "20230414T120000",
    "marketData": {
      "future price": {
        "2023-02-28": 102.0,
        "2023-11-30": 103.0
      }
    }
  },
  {
    "Instrument": "Henry Hub Gas March 24 Future",
    "Time": "20230414T120000",
    "marketData": {
      "future price": {
        "2023-02-1": 102.0,
        "2023-02-28": 103.0
      }
    }
  }
]

```
## Reply:

Azure durable function standard output, use link after "statusQueryGetUri" to see the upload result.

### Note: 

Data will stored in Azure storage in the format marketdata/{Instrument}/{Time}.

## test input calibration data

### Purpose

Upload and save (semi-static) calibration data in Azure storage. They can come from internal/external calibration engine. 

### Address:

[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_calibration_data](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_calibration_data)

### Body example:

```json

[
  {
    "scenario": "scenario-1",
    "Time": "20230414T120000",
    "calibration": {
      "Risk-Free Rate": 0.02,
    }
  }
]
```

## Reply:

Azure durable function standard output, use link after "statusQueryGetUri" to see the upload result.

### Note: 

Data will stored in Azure storage in the format marketdata/{scenario}/{Time}.

## test input contract 

### Purpose

Upload and save option contract to be priced in Azure storage. Then a pricer (Black76) is used to price the option PV and retured in the API 

### Address:

[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_contract_and_run](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_contract_and_run)

### Body example:

``` json
[
  {
    "Contract": "BRN Jan24 Call Strike 100 USD-BBL ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "ICE Brent Jan-24 Future",
      "strike": 100.0,
      "expire date": "2023-11-30",
      "scenario": "scenario-1",
      "pricing date": "2023-1-1"
    }
  },
  {
    "Contract": "HH Mar24 Put Strike 10 USD-MMBTu ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "Henry Hub Gas March 24 Future",
      "strike": 100.0,
      "expire date": "2023-02-28" ,
      "scenario": "scenario-1",
      "pricing date": "2023-1-1"     
    }
  }
]
```

## Reply:

Azure durable function standard output, use link after "statusQueryGetUri" to see the calculation result.

i.e. 
[https://ffqserver.azurewebsites.net/runtime/webhooks/durabletask/instances/dfe8e8a415a24ee1abdff0ec2d3e3ee1?taskHub=FFQServer&connection=Storage&code=t8OJTK-yGKzDhavW4PwvQ4TqKd2rQh95Ke8FOt_7OxBTAzFu2nN3hw==](https://ffqserver.azurewebsites.net/runtime/webhooks/durabletask/instances/dfe8e8a415a24ee1abdff0ec2d3e3ee1?taskHub=FFQServer&connection=Storage&code=t8OJTK-yGKzDhavW4PwvQ4TqKd2rQh95Ke8FOt_7OxBTAzFu2nN3hw==)

In the body of the output, all used inputs and calculated results are displayed.

```json 
[
  {
    "Contract": "BRN Jan24 Call Strike 100 USD-BBL ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "ICE Brent Jan-24 Future",
      "strike": 100.0,
      "expire date": "2023-11-30",
      "scenario": "scenario-1",
      "pricing date": "2023-1-1"
    },
    "underlying market_data": {
      "future price": {
        "2023-02-28": 102.0,
        "2023-11-30": 103.0
      }
    },
    "calibration_data": {
      "Risk-Free Rate": 0.02,
      "Volatility": 0.15
    },
    "Call": 7.351903116724757,
    "Put": 4.379148506992727
  },
  {
    "Contract": "HH Mar24 Put Strike 10 USD-MMBTu ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "Henry Hub Gas March 24 Future",
      "strike": 100.0,
      "expire date": "2023-02-28",
      "scenario": "scenario-1",
      "pricing date": "2023-1-1"
    },
    "underlying market_data": {
      "future price": {
        "2023-02-1": 102.0,
        "2023-02-28": 103.0
      }
    },
    "calibration_data": {
      "Risk-Free Rate": 0.02,
      "Volatility": 0.15
    },
    "Call": 4.203983788652218,
    "Put": 1.2087471263678842
  }
]
```


### Note: 

Contact data will stored in Azure storage in the format marketdata/{Instrument}/{Time}.
