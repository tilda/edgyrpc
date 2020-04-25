# Copyright (c) 2020 S Stewart
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import psutil
from pypresence import Presence
import time
import humanize
from logbook import Logger, StreamHandler
import sys

StreamHandler(sys.stdout).push_application()
log = Logger("edgyrpc")
client_id = "703425123570548746"
rpc = Presence(client_id)


def find_process(name):
    """Returns a list of processes matching the argument `name`"""
    return [p for p in psutil.process_iter(["name"]) if p.info["name"] == name]


def get_memory_usage(process):
    """Adds up all found process memory usage and converts it to human-readable units."""
    info = sum(p.memory_info().rss for p in process)
    usage = humanize.naturalsize(info)
    return usage


rpc.connect()


while True:
    try:
        process = find_process("msedge.exe")
        log.info(f"Found {len(process)} processes")
    except Exception:
        log.critical("No processes found. Exiting")
    if process is not None:
        rpc.update(
            details="<placeholder> tabs open",
            state=f"Using {get_memory_usage(process)} of RAM",
            large_image="browser",
        )
    time.sleep(15)
