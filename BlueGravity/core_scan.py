import asyncio
import gi

gi.require_version("Gtk", "3.0")

from bleak import BleakScanner
from core_receive import device_found


def init_scan(callback):
    def device_find(dev, ad):
        res = device_found(dev, ad)
        if res is None:
            return
        callback(res)

    scanner = BleakScanner(detection_callback=device_find)
    return scanner


async def run_scan(scanner):
    while True:
        await scanner.start()
        await asyncio.sleep(1.0)
        await scanner.stop()
