import os
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, UUID4
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

class FileType(str, Enum):
    WAV = "wav"
    MP4 = "mp4"

class Channels(int, Enum):
    mono = 1
    stereo = 2 


class Extras(BaseModel):
    recordingDevice : str
    driver : str
    channels : Channels
    sampleRateHz : int | float
    bitDepth: int | float
    byteRate : int | float
    gainLevel : int | float

    class Config:
        extra = "forbid" # no extra option


class Record(BaseModel):
    fileId : UUID4
    fileName : str
    fileSizeKB : int | float
    durationSec : int | float
    createdAt : datetime
    filePath: str
    fileType : FileType
    owner: str
    extras : Extras 
    accessCount : int
    categories: list[str]
    description: str

    class Config:
        extra = "forbid" # no extra option


class Ledger(BaseModel):
    record : Record  

    class Config:
        title = "Ledger record"
        description = "A model to validate record entry in Ledger"


LEDGER_DIR = "./src/record/tracker/" 
RECORDINGS_DIR = "./src/record/recordings/"

def ensure_important_directory():
    """
    genrate dir if not present
    """
    ledger_dir = os.path.exists(LEDGER_DIR) 
    recordings_dir = os.path.exists(RECORDINGS_DIR)
    if not ( ledger_dir or recordings_dir):
        print("missing important directory")
    else:
        print("found important directory")
        

def record():
    print("\n\nrecord status checking...")
    ensure_important_directory()
