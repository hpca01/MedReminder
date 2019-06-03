# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
#!/usr/bin/python
import logging

from ask_sdk.standard import StandardSkillBuilder

# from ask_sdk_core.skill_builder import SkillBuilder
from botocore.exceptions import ClientError
from ask_sdk_core.utils import (
    is_request_type,
    is_intent_name,
    get_api_access_token,
    get_slot,
    get_device_id,
)
from ask_sdk_core.handler_input import HandlerInput
from medreminder_utils import user_utils
from medreminder_utils import SSMLHelper, TextHelper, NumberHelper

import requests
import intent_vars
from ask_sdk_core.exceptions import PersistenceException
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.dialog import DelegateDirective, ElicitSlotDirective

sb = StandardSkillBuilder(table_name="Med_Assistant", auto_create_table=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input) -> Response:
    """Handler for Skill Launch."""

    attr = None
    new_user = None

    try:
        attr = handler_input.attributes_manager.persistent_attributes
        speech_text = "Welcome to the KP Pharmacy Assistant, {name}\
                    I can help you get information about your \
                    prescription, as well as set up dosage \
                    and refill reminders. ".format(
            name=attr["user_name"]
        )

    except ClientError as ce:
        if ce.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.log(logging.INFO, msg="Couldn't get user name yet")
        else:
            logger.log(logging.INFO, msg=ce)

    if not attr:
        ssmlhelper = SSMLHelper()
        speech_out = ssmlhelper.get_text_helper()
        attr["user_name"] = ""
        attr["user_new"] = True
        attr["transaction_state"] = "STARTED"
        speech_text = speech_out.speak(
            "Welcome to KP Pharmacy Assistant. Would you like to register?"
        )
        new_user = (
            TextHelper().sentence("Say yes to register or no to quit.").to_string()
        )

    handler_input.attributes_manager.session_attributes = attr

    if new_user:
        return (
            handler_input.response_builder.speak(ssmlhelper.build())
            .ask(new_user)
            .response
        )

    return (
        handler_input.response_builder.speak(speech_text)
        .set_should_end_session(False)
        .response
    )


@sb.request_handler(
    can_handle_func=lambda input: not user_utils.is_user_registered(input)
    and is_intent_name("AMAZON.YesIntent")(input)
)
def yes_handler(handler_input: HandlerInput):
    """handler for Yes Intent if only user is not registered and was asked if they want to register"""
    attr = handler_input.attributes_manager.session_attributes
    attr["user_name"] = handler_input.request_envelope.session.user.user_id.split(".")[
        -1
    ]
    attr[
        "user_access_token"
    ] = handler_input.request_envelope.context.system.api_access_token
    attr["user_new"] = False
    attr["transaction_state"] = "STARTED"

    return handler_input.response_builder.add_directive(
        DelegateDirective(updated_intent=intent_vars.REGISTER_USER)
    ).response


@sb.request_handler(
    can_handle_func=lambda input: not user_utils.is_user_registered(input)
    and is_intent_name("AMAZON.NoIntent")(input)
)
def no_handler(handler_input: HandlerInput):
    ssml = SSMLHelper()
    speech = (
        ssml.get_text_helper()
        .sentence("Thank you for trying KP Pharmacy Assistant.")
        .speak("We're here to help you ")
        .emphasis("thrive", level="moderate")
        .to_string()
    )
    return (
        handler_input.response_builder.speak(speech)
        .set_should_end_session(True)
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name(intent_vars.REGISTER_USER))
def register_user_handler(handler_input: HandlerInput):
    attr = handler_input.attributes_manager.session_attributes
    intent = handler_input.request_envelope.request.intent.to_dict()
    if ("MRN" in intent["slots"]) and ("SSNLastFourDigits" in intent["slots"]):
        ssml = SSMLHelper()
        speech = ssml.get_text_helper()
        attr["MRN"] = intent.get("slots").get("MRN").get("value")
        attr["SSN"] = intent.get("slots").get("SSNLastFourDigits").get("value")
        handler_input.attributes_manager.persistent_attributes = attr
        handler_input.attributes_manager.save_persistent_attributes()
        speech_text = (
            speech.sentence("Thank you for registering.")
            .pause(2)
            .speak("I can get you information about your ")
            .pause(2)
            .emphasis("prescription ", level="moderate")
            .pause(1)
            .speak(" or I can help you set ")
            .pause(1)
            .emphasis(" refill and dosage ", level="moderate")
            .speak(" reminders.")
            .pause(3)
            .speak("What would you like to do?")
            .to_string()
        )
        return handler_input.response_builder.speak(speech_text).response
    else:
        logger.log(logging.INFO, msg="{}{}".format(slots, attr))
        # to log any issues

    return handler_input.response_builder.speak("ERR").response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input) -> Response:
    """Handler for Help Intent."""
    speech_text = "You can say hello to me!"

    return (
        handler_input.response_builder.speak(speech_text)
        .ask(speech_text)
        .set_card(SimpleCard("Hello World", speech_text))
        .response
    )


@sb.request_handler(
    can_handle_func=lambda handler_input: is_intent_name("AMAZON.CancelIntent")(
        handler_input
    )
    or is_intent_name("AMAZON.StopIntent")(handler_input)
)
def cancel_and_stop_intent_handler(handler_input) -> Response:
    """Single handler for Cancel and Stop Intent."""
    speech_text = "Goodbye!"

    return (
        handler_input.response_builder.speak(speech_text)
        .set_card(SimpleCard("Hello World", speech_text))
        .response
    )


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input) -> Response:
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    usn = handler_input.request_envelope.to_dict()
    username = (
        usn.get("session", None).get("user", None).get("user_id", None).split(".")[-1]
    )
    if username:
        usn = username

    speech = (
        "Sorry, {}, The Hello World skill can't help you with that.  "
        "You can say hello!!".format(usn)
    )
    reprompt = "You can say hello!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input) -> Response:
    """Handler for Session End."""
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception) -> Response:
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
