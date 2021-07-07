#! /usr/bin/env python3

import random
import time
import string
import sys

from hashlib import sha1
from requests.exceptions import Timeout

import dtnclient

DESTINATION = "dtn://backbone/"


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

    print(f"{time.time()}: Timestamps for bundle generation: {send_times}", flush=True)

    wait_times = [send_times[0]]
    timestamp = send_times[0]
    for send_time in send_times[1:]:
        wait_times.append(send_time - timestamp)
        timestamp = send_time

    print(f"{time.time()}: Wait times for these timestamps: {wait_times}", flush=True)

    return wait_times


def run(node_name, endpoint_id, payload_size, number_of_bundles, runtime):
    agent_url = "http://localhost:8080/rest"
    initialise_rng(node_name=node_name)

    wait_times = compute_wait_times(runtime, number_of_bundles)

    uuid = dtnclient.register(
        rest_url=agent_url, endpoint_id=endpoint_id
    )["uuid"]

    for sleep_time in wait_times:
        try:
            print(f"{time.time()}: Waiting for {sleep_time} seconds", flush=True)
            time.sleep(sleep_time)

            payload = _generate_payload(payload_size)

            print(f"{time.time()}: Sending bundle", flush=True)
            dtnclient.send_bundle(
                rest_url=agent_url,
                uuid=uuid,
                destination=DESTINATION,
                source=endpoint_id,
                payload=payload,
            )
            print(f"{time.time()}: Bundle sent", flush=True)
        except Timeout:
            print(f"{time.time()}: Sending caused timeout", flush=True)

    print(f"{time.time()}: Done sending", flush=True)
    

def initialise_rng(node_name):
    name_binary = bytes(node_name, encoding="utf8")
    node_seed = sha1(name_binary).digest()
    print(f"{time.time()}: RNG seed: {node_seed}", flush=True)
    random.seed(node_seed)

def _generate_payload(payload_size):
    print(f'{time.time()}: Generating payload')
    payload = "".join(
        random.choices(string.ascii_letters + string.digits, k=payload_size)
    )
    return payload


if __name__ == "__main__":
    this_node = sys.argv[1]
    payload_size = int(sys.argv[2])
    number_of_bundles = int(sys.argv[3])
    runtime = int(sys.argv[4])

    run(this_node, f"dtn://{this_node}/", payload_size, number_of_bundles, runtime)
    print(f"{time.time()}: Terminated", flush=True)