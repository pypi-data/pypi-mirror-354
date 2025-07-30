
import os
import json
import numpy as np

import httpx
import os
from typing import Any

from starlette.requests import Request
from starlette.routing import Mount, Route

import ssl
import datetime
import asyncio

import websocket

g_modelica_src = ""
g_stop_time = 0
g_token = ""
g_url = ""
g_command="o_get_model_linearization"


g_A = None
g_B = None
g_C = None
g_D = None

def on_message_linearization(ws, message):

    global g_command
    global g_A
    global g_B
    global g_C
    global g_D

    try:
        json_obj = json.loads(message)
        if json_obj.get("ws_msg_type") == "response" and json_obj.get("ws_method_param") and json_obj[
            "ws_method_param"].get("command") == g_command:

            if json_obj.get("ws_ret_code") == "SUCCESS" or json_obj.get("ws_ret_code") == "FAILED" or json_obj.get(
                    "ws_ret_code") == "STOPPED":
                # convert_orth2mcp(json_obj)

                if json_obj.get("ws_ret_data"):
                    if json_obj.get("ws_ret_data").get("A") and json_obj["ws_ret_data"]["A"].get("values") is not None:
                        g_A =  np.array(json_obj["ws_ret_data"]["A"].get("values")).reshape( json_obj["ws_ret_data"]["A"].get("shape") )
                    if json_obj.get("ws_ret_data").get("B") and json_obj["ws_ret_data"]["B"].get("values") is not None:
                        g_B =  np.array(json_obj["ws_ret_data"]["B"].get("values")).reshape( json_obj["ws_ret_data"]["B"].get("shape") )
                    if json_obj.get("ws_ret_data").get("C") and json_obj["ws_ret_data"]["C"].get("values") is not None:
                        g_A =  np.array(json_obj["ws_ret_data"]["C"].get("values")).reshape( json_obj["ws_ret_data"]["C"].get("shape") )
                    if json_obj.get("ws_ret_data").get("D") and json_obj["ws_ret_data"]["D"].get("values") is not None:
                        g_A =  np.array(json_obj["ws_ret_data"]["D"].get("values")).reshape( json_obj["ws_ret_data"]["D"].get("shape") )

                ws.close()

    except Exception as e:
        ws.close()


def on_error(ws, error):
    raise ValueError(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    pass


def on_open_get_linearization(ws):

    global g_modelica_src
    global g_stop_time
    global g_command

    global g_A
    global g_B
    global g_C
    global g_D

    g_A = None
    g_B = None
    g_C = None
    g_D = None

    data_dict = {
        "ws_msg_type": "request",
        "ws_method_name": "wsfunc_mb_runcommand",
        "ws_timeout": 30, "ws_seq": "123456780xxx",
        "ws_method_param": {
            "command": g_command,
            "command_param": {
                "mo_src_code": g_modelica_src,
                "mo_stop_time": g_stop_time
            }
        }
    }

    ws.send(json.dumps(data_dict))


def ws_get_linearization( token, url,  mo_src ):

    global g_modelica_src

    global g_A, g_B, g_C, g_D

    g_modelica_src = mo_src

    custom_headers = {
        "Authorization": f"Bearer {token}",
        "Sec-WebSocket-Protocol": token
    }

    ws = websocket.WebSocketApp(
        url.replace("__TASK_ID__", "0"),
        header=custom_headers,
        on_open=on_open_get_linearization,
        on_message=on_message_linearization,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever(
        sslopt={"cert_reqs": ssl.CERT_NONE},
        ping_interval=120,
        ping_timeout=90
    )

    return g_A, g_B, g_C, g_D