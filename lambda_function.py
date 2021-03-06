"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import urllib.request
import json
from twilio.rest import Client

tel = {'johan': +16135522069, 'mitchell': +16478647115, 'parv': +16476071664}
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Weather Network API project. " \
                    "Please ask me an questions relating to weather such as, What is the weather right now?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me an questions relating to weather such as, What is the weather in Kingston Ontario Canada?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Weather Network API project. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def send_sms(information, phoneName):
    # Find these values at https://twilio.com/user/account
    account_sid = "ACa75631f2ff48457ae608c513ad1b5063"
    auth_token = "cfb8a82fecaa3535de4fd52dab2b09c1"

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=tel[phoneName.lower()],
        from_="+16136998144",
        body=information)

def get_bike_alert(intent):
    session_attributes = {}
    reprompt_text = None
    tMin = []
    rain = []
    
    URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword=London&prov=ON&country=Canada&locale=en-US"
    response = urllib.request.urlopen(URL)
    info = json.loads(response.read())
    #print (info["code"])
    data_ob = "https://hackathon.pic.pelmorex.com/api/data/shortterm?locationcode="+info["code"]
    response_2 = urllib.request.urlopen(data_ob)
    observation = json.loads(response_2.read())
    for dat in observation["data"]:
        tMin.append(dat["tempMin"])
        rain.append(dat["rain"])
    rVal = (float)(rain[0])
    tVal = (float)(tMin[0])
    if rVal > 1:
        speech_output = "London has chances of rain and I would recommend not to "+ intent['slots']['TranspoMethod']['value'] +". It might be better to take the car today."
    elif tVal < 5:
        speech_output = "London has a fairly low temperature and I would recommend not to "+ intent['slots']['TranspoMethod']['value'] +". It might be better to take the car today."
    else:
        speech_output = "London has a good weather condition today so you can "+ intent['slots']['TranspoMethod']['value'] +" today."
        
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def send_weather_info(intent):
    session_attributes = {}
    reprompt_text = None
    speech_output = None
    should_end_session = False
    
    city = intent['slots']['City']
    region = intent['slots']['Region']
    country = intent['slots']['Country']
    
    print (intent)
    print ((('value' in city) and ('value' in region) and ('value' in country)))
    print ((('value' not in city) and ('value' not in region) and ('value' not in country)))
    
    if (('value' in city) and ('value' in region) and ('value' in country)):
        # Must replace spaces with "+"
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword="+city['value'].replace(" ","+")+"&prov="+region['value'].replace(" ","+")+"&country="+country['value'].replace(" ","+")+"&locale=en-US"
    elif (('value' not in city) and ('value' not in region) and ('value' not in country)):
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword=London&prov=ON&country=Canada&locale=en-US"
    else:
        speech_output = "Please specify the city, region and country together."
                        
        reprompt_text = "I'm not sure what place you are referring to. " \
                        "You can ask me about the weather by saying, What is the weather in London Ontario Canada"
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))
    
    response = urllib.request.urlopen(URL)
    info = json.loads(response.read())
    #print (info["code"])
    if('value' in intent['slots']['Date']):
        data_ob = "https://hackathon.pic.pelmorex.com/api/weather/date/?locationcode="+info["code"]+"&date="+intent['slots']['Date']['value']+"&unit=C&locale=en-CA"
    else:
        data_ob = "https://hackathon.pic.pelmorex.com/api/weather/date/?locationcode="+info["code"]+"&unit=C&locale=en-CA"
    response = urllib.request.urlopen(data_ob)
    observation = json.loads(response.read())
    
    speech_output = observation["speech"]
    should_end_session = True
    send_sms(speech_output, intent['slots']['PhoneName']['value'])
    speech_output = "Sending SMS to "+ intent['slots']['PhoneName']['value'] +" containing the following information." + speech_output
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
def get_weather_by_date(intent):
    session_attributes = {}
    reprompt_text = None
    speech_output = None
    should_end_session = False
    
    city = intent['slots']['City']
    region = intent['slots']['Region']
    country = intent['slots']['Country']
    
    print (intent)
    print ((('value' in city) and ('value' in region) and ('value' in country)))
    print ((('value' not in city) and ('value' not in region) and ('value' not in country)))
    
    if (('value' in city) and ('value' in region) and ('value' in country)):
        # Must replace spaces with "+"
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword="+city['value'].replace(" ","+")+"&prov="+region['value'].replace(" ","+")+"&country="+country['value'].replace(" ","+")+"&locale=en-US"
    elif (('value' not in city) and ('value' not in region) and ('value' not in country)):
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword=London&prov=ON&country=Canada&locale=en-US"
    else:
        speech_output = "Please specify the city, region and country together."
                        
        reprompt_text = "I'm not sure what place you are referring to. " \
                        "You can ask me about the weather by saying, What is the weather in London Ontario Canada"
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))
    
    response = urllib.request.urlopen(URL)
    info = json.loads(response.read())
    #print (info["code"])
    data_ob = "https://hackathon.pic.pelmorex.com/api/weather/date/?locationcode="+info["code"]+"&date="+intent['slots']['Date']['value']+"&unit=C&locale=en-CA"
    response = urllib.request.urlopen(data_ob)
    observation = json.loads(response.read())
    
    speech_output = observation["speech"]
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_weather_observation(intent):
    session_attributes = {}
    reprompt_text = None
    speech_output = None
    should_end_session = False
    
    city = intent['slots']['City']
    region = intent['slots']['Region']
    country = intent['slots']['Country']
    
    print (intent)
    print ((('value' in city) and ('value' in region) and ('value' in country)))
    print ((('value' not in city) and ('value' not in region) and ('value' not in country)))
    
    if (('value' in city) and ('value' in region) and ('value' in country)):
        cityPhrase = city['value']
        # Must replace spaces with "+"
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword="+city['value'].replace(" ","+")+"&prov="+region['value'].replace(" ","+")+"&country="+country['value'].replace(" ","+")+"&locale=en-US"
    elif (('value' not in city) and ('value' not in region) and ('value' not in country)):
        cityPhrase = "London"
        URL = "https://hackathon.pic.pelmorex.com/api/search/string?keyword=London&prov=ON&country=Canada&locale=en-US"
    else:
        speech_output = "Please specify the city, region and country together."
                        
        reprompt_text = "I'm not sure what place you are referring to. " \
                        "You can ask me about the weather by saying, What is the weather in London Ontario Canada"
        return build_response(session_attributes, build_speechlet_response(
            intent['name'], speech_output, reprompt_text, should_end_session))
    
    response = urllib.request.urlopen(URL)
    info = json.loads(response.read())
    #print (info["code"])
    data_ob = "https://hackathon.pic.pelmorex.com/api/data/observation?locationcode="+info["code"]
    response = urllib.request.urlopen(data_ob)
    observation = json.loads(response.read())
    
    speech_output = "The temperature in " + cityPhrase +" is " + observation["data"]["temp"] + " degrees celsius."
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def champions(intent):
    session_attributes = {}
    reprompt_text = None
        
    speech_output = "I was created by the team with the best use of the Weather Network API."
    should_end_session = True

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "WeatherObservation":
        return get_weather_observation(intent)
    elif intent_name == "BikeAlert":
        return get_bike_alert(intent)
    elif intent_name == "WeatherDate":
        return get_weather_by_date(intent)
    elif intent_name == "SendWeatherInfo":
        return send_weather_info(intent)
    elif intent_name == "Champions":
        return champions(intent)    
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])