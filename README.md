# The Weather Network API integration with Amazon Echo (Alexa)
An Amazon Alexa skill set created for integration with The Weather Network REST API.

## The Idea


## Command Types
* Current Weather Information: What is the weather?
  * See sample commands [here](docs/README_Basic.md)
* Weather Information by date: What is the weather on Thursday?
  * See sample commands [here](docs/README_Date.md)
* Transportation Method: Should I bike to work today?
  * See sample commands [here](docs/README_Transportation.md)
* Text Message: Send a text message to Mitchell with weather for Kingston Ontario Canada for tomorrow.
  * See sample commands [here](docs/README_TextMessage.md)
* Champions: What team made the best use of The Weather Network API?
  * See sample commands [here](docs/README_Champions.md)

## The Code
* lambda_function.py
* language_model/language_model.json

## Tools Used
* Amazon Developer Console : https://developer.amazon.com/
 * Used Amazon Alexa Skills Kit to add new custom skills to Alexa.
 * Details:
  Skill Name: WeatherNetwork
  Invocation Name: The Weather Network (The name customers use to activate the skill. For example, "Alexa ask Tide Pooler...")
  Service EndPoint Type: AWS Lambda ARN
  Default EndPoint: arn:aws:lambda:us-east-1:542432488227:function:myColorPython
 * See language_model/language_model.json for Interaction Model Specification
* Amazon AWS Lambda : https://console.aws.amazon.com/lambda/
 * Runtime Language: Python 3.6
 * See lambda_function.py for python runtime code.
 * ZIP full repo into a .zip file for AWS Lambda upload to ensure all neccessary python modules are included. 

## How to use

## References/Resources
 * Amazon Developer Console - https://developer.amazon.com/
 * Amazon AWS Lambda - https://console.aws.amazon.com/lambda/
 * Amazon Alexa Interface - https://alexa.amazon.com/spa/index.html#cards
 * STDLIB (JS alternative to Amazon AWS Lambda) - https://stdlib.com 
 * STDLIB with Alexa Quick Start Guide - https://hackernoon.com/build-an-alexa-skill-in-7-minutes-flat-with-node-js-and-stdlib-70611f58c37f

## Expansion Ideas
 * MMS Trend Graphs

## Authors
* Parv Mital
* Johan Cornelissen
