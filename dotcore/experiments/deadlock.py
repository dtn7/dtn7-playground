#! /usr/bin/env python3

import os
import time
import shutil
import glob
import logging
import re
import sys

from datetime import datetime

from core.emulator.coreemu import CoreEmu
from core.emulator.enumerations import EventTypes
from core.services import ServiceManager


def collect_logs(session_dir, runtime, bpn, payload, dest_dir="/tmp/results"):
    exclude = [r"store_.*", r"var.run", r"var.log"]
    os.makedirs(dest_dir, exist_ok=True)

    with open(f"{dest_dir}/experiment.conf", "w") as conf_file:
        conf_file.write(
            f"runtime: {runtime}\nbundles per node: {bpn}\npayload size: {payload}\n"
        )

    for node_dir in glob.glob(f"{session_dir}/*.conf"):
        _, node_name = os.path.split(node_dir)
        node_dest = os.path.join(dest_dir, node_name)
        os.makedirs(node_dest, exist_ok=True)

        for content_path in glob.glob(f"{node_dir}/*"):
            _, content_name = os.path.split(content_path)

            if any(re.match(regex, content_name) for regex in exclude):
                logging.info(f"skipping {content_path}")
                continue

            logging.info(f"copying {content_path}")
            content_dest = os.path.join(node_dest, content_name)
            if os.path.isdir(content_path):
                shutil.copytree(content_path, content_dest)
            else:
                shutil.copy(content_path, content_dest)


def check_success(session_dir):
    for node_dir in glob.glob(f"{session_dir}/*.conf"):
        with open(f"{node_dir}/traffic_generator_run.log", "r") as log_file:
            if "Sending caused timeout" in log_file.read():
                return 1

    return 0


if __name__ in ["__main__", "__builtin__"]:
    logging.basicConfig(level=logging.DEBUG, force=True)

    logging.info("Gathering experiment settings.")
    runtime = int(os.environ.get("EXPERIMENT_RUNTIME", 60))
    bpn = int(os.environ.get("BUNDLES_PER_NODE", 6))
    payload = int(os.environ.get("PAYLOAD_SIZE", 1024))

    logging.info("Setting up CORE.")
    coreemu = CoreEmu()
    session = coreemu.create_session()
    session.set_state(EventTypes.CONFIGURATION_STATE)
    print(ServiceManager.add_services("/root/.core/myservices"))

    logging.info("Starting virtual nodes.")
    session.open_xml(file_name="/root/.core/configs/deadlock.xml", start=True)
    time.sleep(10)

    logging.info(f"Experiment is running for {runtime} seconds.")
    time.sleep(runtime)

    session.set_state(EventTypes.DATACOLLECT_STATE)

    logging.info("Checking logs if something went wrong.")
    return_code = check_success(session.session_dir)

    logging.info("Collecting logs.")
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dest_dir = f"/tmp/results/{now}"
    collect_logs(session.session_dir, runtime, bpn, payload, dest_dir=log_dest_dir)

    logging.info("Shutting down CORE.")
    coreemu.shutdown()
    os.system("core-cleanup")

    logging.info("Experiment finished.")

    if return_code != 0:
        logging.error("Experiment failed due to timeout.")

    sys.exit(return_code)
