#! /usr/bin/env python3

import random
import time
import string
import requests
import json
import argparse
import platform
import logging
import os

from hashlib import sha1
from requests.exceptions import Timeout

REQUEST_TIMEOUT = 60

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "--destination",
    help="destination to send bundles to",
    default="dtn://backbone/",
)
parser.add_argument(
    "-s",
    "--source",
    help="source endpoint id to send bundles from",
    default=f"dtn://{platform.node()}/",
)
parser.add_argument(
    "-b",
    "--bytes",
    help="size of the payload to be generated (bytes)",
    type=int,
    default=os.environ.get("PAYLOAD_SIZE", default=1024),
)
parser.add_argument(
    "-c",
    "--count",
    help="number of bundles to send during program runtime",
    type=int,
    default=os.environ.get("BUNDLES_PER_NODE", default=6),
)
parser.add_argument(
    "-r",
    "--runtime",
    help="program runtime in seconds",
    type=int,
    default=os.environ.get("EXPERIMENT_RUNTIME", default=60),
)


class RESTError(Exception):
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return f"RESTError happened: {self.status_code} - {self.error}"


def register(rest_url, endpoint_id, registration_data_file=""):
    id_json = json.dumps({"endpoint_id": endpoint_id})
    response = requests.post(f"{rest_url}/register", data=id_json, timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise RESTError(status_code=response.status_code, error=response.text)

    parsed_response = response.json()
    if parsed_response["error"]:
        raise RESTError(status_code=response.status_code, error=parsed_response["error"])

    data = {"endpoint_id": endpoint_id, "uuid": parsed_response["uuid"]}
    marshaled = json.dumps(data)
    if registration_data_file:
        with open(registration_data_file, "w") as f:
            f.write(marshaled)
    return data


def send_bundle(rest_url, uuid, source, destination, payload, lifetime="24h"):
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

    response = requests.post(f"{rest_url}/build", data=json.dumps(data), timeout=REQUEST_TIMEOUT)
    if response.status_code != 200:
        raise RESTError(status_code=response.status_code, error=response.text)

    parsed_response = response.json()
    if parsed_response["error"]:
        raise RESTError(status_code=response.status_code, error=parsed_response["error"])


def compute_wait_times(t_stop, count):
    send_times = []
    runtime = t_stop - 10
    slot_length = int(runtime / count)

    slot_start = 10
    slot_stop = 10 + slot_length
    while len(send_times) < count:
        send_time = random.randint(slot_start, slot_stop)
        send_times.append(send_time)
        slot_start = slot_stop + 1
        slot_stop = slot_start + slot_length

    logging.info(f"Timestamps for bundle generation: {send_times}")

    wait_times = [send_times[0]]
    timestamp = send_times[0]
    for send_time in send_times[1:]:
        wait_times.append(send_time - timestamp)
        timestamp = send_time

    logging.info(f"Wait times for these timestamps: {wait_times}")

    return wait_times


def run(source, bytes, count, runtime, destination, **kwargs):
    agent_url = "http://localhost:8080/rest"
    initialise_rng(node_name=source)

    wait_times = compute_wait_times(runtime, count)

    uuid = register(rest_url=agent_url, endpoint_id=source)["uuid"]

    for sleep_time in wait_times:
        try:
            logging.info(f"Waiting for {sleep_time} seconds")
            time.sleep(sleep_time)

            payload = _generate_payload(bytes)

            logging.info(f"Sending bundle")
            send_bundle(
                rest_url=agent_url,
                uuid=uuid,
                destination=destination,
                source=source,
                payload=payload,
            )
            logging.info(f"Bundle sent")
        except Timeout:
            logging.info(f"Sending caused timeout")

    logging.info(f"Done sending")


def initialise_rng(node_name):
    name_binary = bytes(node_name, encoding="utf8")
    node_seed = sha1(name_binary).digest()
    logging.info(f"RNG seed: {node_seed}")
    random.seed(node_seed)


def _generate_payload(payload_size):
    logging.info("Generating payload")
    payload = "".join(random.choices(string.ascii_letters + string.digits, k=payload_size))
    return payload


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    args = parser.parse_args()
    run(**args.__dict__)

    logging.info("Terminated")