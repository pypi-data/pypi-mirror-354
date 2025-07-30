
import os
import json

import numpy as np
from typing import Union, Tuple
# from src.orthpylib.ws_lib import ws_get_linearization
from .ws_lib import ws_get_linearization

def get_orth_token():
    token_str = os.getenv("LOCALSTORAGE_ORTHOGONAL_HOST", "")
    host_str = os.getenv("LOCALSTORAGE_ORTHOGONAL_TOKEN", "")
    # token_str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5ODAzMjk0LCJpYXQiOjE3NDkxOTg0OTQsImp0aSI6IjUyZWU4YzA4MjE2MDRjYmI4YzdlYjU2YTI4OTg5ZjM4IiwidXNlcl9pZCI6OH0.4UbjdSjvmnaGDeqSQ26ekkmBhL2fpOxqiW64iz1VYU8"
    # host_str = f"ws://192.168.116.130/ws/commontask/__TASK_ID__/"
    return True, f"", token_str, host_str


    if len(token_str) == 0 or len(host_str)==0:
        return False, f"env var missing", None, None

    try:
        data = json.loads(token_str)
        if data.get('access') is None:
            return False, f"env var invalid access", None, None

        return True, f"", data.get('access').strip(), host_str.strip()

    except json.JSONDecodeError as e:
        return False, f"env var invalid", None, None

    return False, f"Failed to get token", "", ""


def get_linearization_matrix( mo_src_code ):
    ret, msg, token, url= get_orth_token()

    if url is None or len(url)==0:
        raise ValueError(f"env LOCALSTORAGE_ORTHOGONAL_HOST missing {msg}")

    if token is None or len(token)==0:
        raise ValueError(f"env LOCALSTORAGE_ORTHOGONAL_TOKEN missing {msg}")

    a, b, c, d = ws_get_linearization( token, url, mo_src_code )

    return a, b, c, d
