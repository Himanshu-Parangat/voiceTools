import os, json
from uuid import uuid4
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
LEDGER_DATA = []

def ensure_important_directory():
    """
    genrate dir if not present
    """
    print("\n\nchecking important directory")
    if not os.path.exists(LEDGER_DIR):
        print("genrateing missing Ledger directory")
        os.mkdir(LEDGER_DIR)
    else:
        print("Ledger directory located.")


    if not os.path.exists(RECORDINGS_DIR):
        print("genrateing missing Recording directory")
        os.mkdir(RECORDINGS_DIR)
    else:
        print("Recording directory located.")


LEDGER_FILE = "./src/record/tracker/ledger.json" 
def ensure_ledger_exist():
    """
    create Ledger.json if not exists
    """
    if not os.path.exists(LEDGER_FILE):
        print("No previous ledger found")
        with open(LEDGER_FILE,"w") as ledger:
            json.dump(LEDGER_DATA,ledger,indent=2)
            print(f"wrinting empty {LEDGER_DATA} ...")
    else:
        print("found existing Ledger.")


def genrate_ledger() -> dict:
    sample_extras = Extras(
        recordingDevice="blutooth ex 2p1",
        driver="ffmpeg",
        channels=Channels.stereo,
        sampleRateHz=48000,
        bitDepth=24,
        byteRate=96000,
        gainLevel=5.0
    )

    sample_record = Record(
        fileId= uuid4(), 
        fileName="sample_audio.wav",
        fileSizeKB=5120.5,
        durationSec=300.0,
        createdAt=datetime.now(),
        filePath="/path/to/sample_audio.wav",
        fileType=FileType.WAV,
        owner="John Doe",
        extras=sample_extras,
        accessCount=2,
        categories=["vocal fry", "pitch training"],
        description="A sample audio file for testing."
    )

    sample_ledger = Ledger(record=sample_record)

    new_data : dict = sample_ledger.model_dump(mode='json')

    return new_data

def append_record(new_record):
    """
    append data
    """
    print("reading ledger")

    with open(LEDGER_FILE,"r") as ledger:
        ledger_data : list["Any"] = json.load(ledger)

    ledger_data.append(new_record)
    
    with open(LEDGER_FILE,"w") as ledger:
        json.dump(ledger_data,ledger,indent=2)

    print("updated ledger")


def record():
    print("\n\nrecord status checking...")
    ensure_important_directory()
    ensure_ledger_exist()
    append_record(genrate_ledger())
