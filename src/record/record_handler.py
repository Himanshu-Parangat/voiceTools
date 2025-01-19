import sounddevice as sd
from typing import Any, Dict, List


def get_default_device():
    try:
        return sd.default.device
    except Exception as e:
        raise e


# def list_devices():
#     devices = sd.query_devices()
#     print("Available Devices:")
#     for i, device in enumerate(devices):
#         print(f"{i}: {device['name']}")


def list_devices():
    devices: List[Dict[str, Any]] = sd.query_devices() # type: ignore 
    print("Available Devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device.get('name', 'Unknown Device')}")



def get_all_device():
    devices = sd.query_devices()
    try:
        devices = sd.query_devices()
        if devices:
            print("Available devices:")
            return devices
        else:
            print("No devices found.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")


def check_input_settings(device_name):
    try:
        print("Input settings are valid.")
        sd.check_input_settings(device=device_name)
        return True
    except Exception as e:
        print(f"Input settings error: {e}")
        return False

def record():
    print("\n\nrecord status checking...")




