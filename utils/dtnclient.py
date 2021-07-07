#! /usr/bin/env python3

import requests
import json


REQUEST_TIMEOUT = 60


class RESTError(Exception):
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.errir = error

    def __str__(self):
        return f"RESTError happened: {self.status_code} - {self.error}"


def register(rest_url, endpoint_id, registration_data_file = ""):
    id_json = json.dumps({"endpoint_id": endpoint_id})
    response = requests.post(f"{rest_url}/register", data=id_json, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise RESTError(status_code=response.status_code, error=response.text)

    parsed_response = response.json()
    if parsed_response["error"]:
        raise RESTError(
            status_code=response.status_code, error=parsed_response["error"]
        )

    data = {"endpoint_id": endpoint_id, "uuid": parsed_response["uuid"]}
    marshaled = json.dumps(data)
    if registration_data_file:
        with open(registration_data_file, "w") as f:
            f.write(marshaled)
    return data


def send_bundle( rest_url, uuid, source, destination, payload, lifetime = "24h"):
    data = {
        "uuid": uuid,
        "arguments": {
            "destination": destination,
            "source": source,
            "creation_timestamp_now": 1,
            "lifetime": lifetime,
            "payload_block": payload,
        },
    }

    response = requests.post(
        f"{rest_url}/build", data=json.dumps(data), timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise RESTError(status_code=response.status_code, error=response.text)

    parsed_response = response.json()
    if parsed_response["error"]:
        raise RESTError(
            status_code=response.status_code, error=parsed_response["error"]
        )
