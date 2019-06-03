#!/usr/bin/python

from ask_sdk_core.handler_input import HandlerInput


def is_user_registered(handler_input: HandlerInput) -> bool:
    """
    default state of func is not registered
    """
    is_registered = False

    session_attr = handler_input.attributes_manager.session_attributes

    if "user_new" in session_attr and (
        (session_attr["user_new"] == False) or session_attr["user_new"] == "false"
    ):
        is_registered = True

    return is_registered
