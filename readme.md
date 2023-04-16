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

# test input:

## market data

API: 


[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_market_data](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_market_data)

Body:
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



## test input calibration data


API: 

[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_calibration_data](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_calibration_data)

Body:

```json

[
  {
    "scenario": "scenario-1",
    "Time": "20230414T120000",
    "calibration": {
      "Risk-Free Rate": 0.02,
      "dividend/carry on cost": -0.01
    }
  }
]
```

## test input contract 

API: 

[https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_contract_and_run](https://ffqserver.azurewebsites.net/api/orchestrators/ffq_test2/upload_contract_and_run)

Body:

``` json

[
  {
    "Instrument": "BRN Jan24 Call Strike 100 USD/BBL ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "ICE Brent Jan-24 Future",
      "strike": 100.0,
      "expire date": "2023-11-30"
    },
      "scenario": "scenario-1"
  },
  {
    "Instrument": "HH Mar24 Put Strike 10 USD/MMBTu ",
    "Time": "20230414T120000",
    "contractData": {
      "Underlying": "Henry Hub Gas March 24 Future",
      "strike": 100.0,
      "expire date": "2023-02-29"      
    },
      "scenario": "scenario-1"
  }
]
```

## test output

click the "statusQueryGetUri" in the reply of the contract upload API
i.e. 
[https://ffqserver.azurewebsites.net/runtime/webhooks/durabletask/instances/86f3df8e146948a796e766ac80e33db8?taskHub=FFQServer&connection=Storage&code=t8OJTK-yGKzDhavW4PwvQ4TqKd2rQh95Ke8FOt_7OxBTAzFu2nN3hw==](https://ffqserver.azurewebsites.net/runtime/webhooks/durabletask/instances/86f3df8e146948a796e766ac80e33db8?taskHub=FFQServer&connection=Storage&code=t8OJTK-yGKzDhavW4PwvQ4TqKd2rQh95Ke8FOt_7OxBTAzFu2nN3hw==)


including used contract, marketdata and calibration data inputs

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
    "market_data": {
      "future price": {
        "2023-02-28": 102.0,
        "2023-11-30": 103.0
      }
    },
    "calibration_data": {
      "Risk-Free Rate": 0.02,
      "dividend/carry on cost": -0.01,
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
    "market_data": {
      "future price": {
        "2023-02-1": 102.0,
        "2023-02-28": 103.0
      }
    },
    "calibration_data": {
      "Risk-Free Rate": 0.02,
      "dividend/carry on cost": -0.01,
      "Volatility": 0.15
    },
    "Call": 4.203983788652218,
    "Put": 1.2087471263678842
  }
]
```
