# Copyright (c) 2020 S Stewart
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import psutil
from pypresence import Presence
import humanize
from logbook import Logger, StreamHandler
import sys
import websockets
import asyncio

StreamHandler(sys.stdout).push_application()
log = Logger("edgyrpc")
client_id = "703425123570548746"
rpc = Presence(client_id)

rpc.connect()

def find_process(name):
    """Returns a list of processes matching the argument `name`"""
    return [p for p in psutil.process_iter(["name"]) if p.info["name"] == name]


def get_memory_usage(process):
    """Adds up all found process memory usage and converts it to human-readable units."""
    info = sum(p.memory_info().rss for p in process)
    usage = humanize.naturalsize(info)
    return usage

async def main(ws, path):
    while True:
        try:
            tabs = await ws.recv()
            log.info(f'Received: {tabs} tabs')
        except websockets.exceptions.ConnectionClosedOK:
            pass # why is this an error
        try:
            process = find_process("msedge.exe")
            log.info(f'Found {len(process)} processes')
        except Exception:
            log.exception('Something happened?')
        try:
            rpc.update(
                details=f'{tabs} tab{"s" if tabs > 1 else ""} open',
                state=f'Using {get_memory_usage(process)} of RAM',
                large_image="browser"
            )
        except:
            pass # shove ur error up ur ugly ass

        await ws.send('OK')

socket = websockets.serve(main, "localhost", 3233)

loop = asyncio.get_event_loop()
loop.run_until_complete(socket)
log.info("Starting...")
loop.run_forever()
