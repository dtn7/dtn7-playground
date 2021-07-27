#! /usr/bin/env python3

import os
import time
import tarfile
import glob
import logging


from datetime import datetime

from core.emulator.coreemu import CoreEmu
from core.emulator.enumerations import EventTypes
from core.services import ServiceManager


def collect_logs(session_dir):
    now = datetime.now()
    now_formatted = now.strftime("%Y%m%d_%H%M%S")

    node_logs_to_collect = ["dtnd_run.log", "dtnd.toml", "traffic_generator_run.log"]

    with tarfile.open(f"/results/{now_formatted}.tar.gz", "w:gz") as tar:
        core_log = "/var/log/core-daemon.log"
        tar.add(core_log, arcname=os.path.basename(core_log))

        for node_dir in glob.glob(f"{session_dir}/*.conf"):
            for log in node_logs_to_collect:
                abs_log_path = f"{node_dir}/{log}"
                rel_log_path = abs_log_path.replace(f"{session_dir}/", "")
                tar.add(abs_log_path, arcname=rel_log_path)


if __name__ in ["__main__", "__builtin__"]:
    logging.basicConfig(level=logging.DEBUG, force=True)

    logging.info("Gathering experiment settings.")
    runtime = int(300)

    logging.info("Setting up CORE.")
    coreemu = CoreEmu()
    session = coreemu.create_session()
    session.set_state(EventTypes.CONFIGURATION_STATE)
    print(ServiceManager.add_services("/root/.core/myservices"))

    logging.info("Starting virtual nodes.")
    session.open_xml(file_name="/root/.core/configs/scenario.xml", start=True)
    time.sleep(10)

    # Run the experiment
    logging.info(f"Experiment is running for {runtime} seconds.")
    time.sleep(runtime)

    # When the experiment is finished, we set the session to
    # DATACOLLECT_STATE and collect the logs.
    # After that, we shutdown the session, cleanup the generated payloads
    # and manually make sure, that all remaining files of the experiments
    # are gone.
    # Finally, we wait another 10 seconds to make sure everyhing is clean.
    logging.info("Collecting logs.")
    session.set_state(EventTypes.DATACOLLECT_STATE)
    time.sleep(2)
    collect_logs(session.session_dir)

    logging.info("Shutting down CORE.")
    coreemu.shutdown()
    os.system("core-cleanup")
    time.sleep(10)

    logging.info("Experiment finished.")