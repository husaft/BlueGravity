from datetime import datetime
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from construct.core import ConstError
from core_structs import create_yohealth

yohealth_format = create_yohealth()


def device_found(device: BLEDevice, advertisement_data: AdvertisementData):
    now = datetime.now()
    try:
        name = advertisement_data.local_name
        if name is None or name != 'YoHealth':
            return
        signal = advertisement_data.rssi
        addr = device.address
        data = advertisement_data.manufacturer_data[0xA102]
        raw = data.hex()
        parsed = yohealth_format.parse(data)
        weight = parsed.weight / 10.0
        is_final = parsed.type != -128
        iso_date = now.isoformat()
        return {'t': iso_date, 's': signal, 'a': addr, 'n': name, 'r': raw, 'w': weight, 'f': is_final}
    except KeyError:
        pass
    except ConstError:
        pass
