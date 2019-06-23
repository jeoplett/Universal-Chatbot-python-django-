# coding: utf8

import requests
from . import app_config
import datetime

def pushUnknownResponse(unified_message):
    try:
        try:
            last_name = unified_message['last_name']
        except Exception:
            last_name = "_empty_"
        try:
            first_name = unified_message['first_name']
        except Exception:
            first_name = "_empty_"
        command = unified_message['last_chat_trigger']['command'] + " - " + unified_message['new_chat_trigger']['command']
        request_data = {"api_token": unified_message['bot_api_token'], "type": "unknown_response", "chat_id": unified_message['chat_id'], "command": command, "message": unified_message['new_chat_record']['last_chat_message'], "first_name": first_name, "last_name": last_name}
        request = requests.get(app_config.getStatServiceURL(), params = request_data)
    except Exception:
        return ""
    return ""
    

def pushForm(unified_message):
    try:
        try:
            last_name = unified_message['last_name']
        except Exception:
            last_name = "_empty_"
        try:
            first_name = unified_message['first_name']
        except Exception:
            first_name = "_empty_"
        command = unified_message['last_chat_trigger']['command'] + " - " + unified_message['new_chat_trigger']['command']
        request_data = {"api_token": unified_message['bot_api_token'], "type": "push", "chat_id": unified_message['chat_id'], "command": command, "message": unified_message['new_chat_record']['last_chat_message'], "first_name": first_name, "last_name": last_name}
        request = requests.get(app_config.getStatServiceURL(), params = request_data)
    except Exception:
        return ""
    return ""

def pushInfo(unified_message):
    try:
        try:
            last_name = unified_message['last_name']
        except Exception:
            last_name = "_empty_"
        try:
            first_name = unified_message['first_name']
        except Exception:
            first_name = "_empty_"
        command = unified_message['last_chat_trigger']['command'] + " - " + unified_message['new_chat_trigger']['command']
        request_data = {"api_token": unified_message['bot_api_token'], "type": "info", "chat_id": unified_message['chat_id'], "command": command, "message": unified_message['new_chat_record']['last_chat_message'], "first_name": first_name, "last_name": last_name}
        request = requests.get(app_config.getStatServiceURL(), params = request_data)
    except Exception:
        return ""
    return ""

def pushSystemEvent(system_event_message):
    try:
        request_data = {"api_token": app_config.getSystemAPIToken(), "type": "system_event", "message": "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + system_event_message}
        request = requests.get(app_config.getStatServiceURL(), params = request_data)
    except Exception:
        return ""
    return ""
