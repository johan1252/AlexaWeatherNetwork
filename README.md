# The Weather Network API integration with Amazon Echo (Alexa)
An Amazon Alexa skill set created for integration with The Weather Network REST API.

## The Idea
The intention of this project was to make use of The Weather Network API in a creative fashion.
This was done through the use of the developer tools provided with Amazon Alexa. A custom skill set
that can be invoked using "Alexa, ask The Weather Network \<command\>" was created. The skill set 
provides basic weather information for the current location currently or on a future date. Additionally
the functionality was extended to provide recommendations on the type of transportation to use when travelling 
to work or school. The system can also send individuals an SMS with relevant weather information with the 
simple use of a voice command. The project was created during a 36 hour hacking period at Hack Western 4.

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
	* Python code for all backend command processing.
	* Created to run on Amazon Lambda server with all necessary python modules being provided in this repo.
	* See "How to use" section for more information on how to get started.
* language_model/language_model.json
	* Intents, Custom Slot Types, and Utterances for use by Amazon Alexa Developer console.
	* Used in an interactive model for interaction between human and echo.
	* See "How to use" section for more information on how to get started.

## Tools Used
* Amazon Developer Console : https://developer.amazon.com/
  * Used Amazon Alexa Skills Kit to add new custom skills to Alexa.
  * Details:
    * Skill Name: WeatherNetwork
    * Invocation Name: The Weather Network (The name customers use to activate the skill. For example, "Alexa ask Tide Pooler...")
    * Service EndPoint Type: AWS Lambda ARN
    * Default EndPoint: arn:aws:lambda:us-east-1:542432488227:function:myColorPython
    * See language_model/language_model.json for Interaction Model Specification
* Amazon AWS Lambda : https://console.aws.amazon.com/lambda/
  * Runtime Language: Python 3.6
  * See lambda_function.py for python runtime code.
  * ZIP full repo into a .zip file for AWS Lambda upload to ensure all neccessary python modules are included. 

## How to use
1. Create an Amazon Developer Account at https://developer.amazon.com/
2. Create an Amazon AWS Lambda function using https://console.aws.amazon.com/lambda/
	1. Ensure runtime Language is set to Python 3.6.
	2. Handler is set to "lambda_function.lambda_handler".
	3. The "Alexa Skills Kit" trigger is added to the function.
	4. Make note of the ARN (Amazon Resource Name) noted at the top of the webpage for future use.
	5. Upload a ZIP archive (make a ZIP at the top level of this repo to ensure all python libraries are included) to the Lambda function.
3. In the Amazon Developer Console
	1. Create a new custom skill for Amazon Alexa using the following:
		1. Name: WeatherNetwork
		2. Invocation Name: The Weather Network
		3. For Interaction Model use JSON found in language_model/language_model.json
		4. Service EndPoint Type: AWS Lambda ARN
		5. Default EndPoint: \<your ARN address from step 2\>
		6. Test your custom skill set appropriately.
4. You're all set! You are now ready to use Amazon Alexa with the custom Weather Network API.

## References/Resources
 * Amazon Developer Console - https://developer.amazon.com/
 * Amazon AWS Lambda - https://console.aws.amazon.com/lambda/
 * Amazon Alexa Interface - https://alexa.amazon.com/spa/index.html#cards
 * STDLIB (JS alternative to Amazon AWS Lambda) - https://stdlib.com 
 * STDLIB with Alexa Quick Start Guide - https://hackernoon.com/build-an-alexa-skill-in-7-minutes-flat-with-node-js-and-stdlib-70611f58c37f

## Expansion Ideas
 * MMS Trend Graphs
 	* Allow users to send trend graphs such as wind speed, min and max temperature, etc. for the last 7 days to a user's cell phone. This expands on the current SMS capability to allow MMS messages. Where valuable statistics can be presented in graphical format.
	* Example created:
	* ![Alt text](sampleTrendGraph.png?raw=true)

## Authors
* Parv Mital
* Johan Cornelissen
