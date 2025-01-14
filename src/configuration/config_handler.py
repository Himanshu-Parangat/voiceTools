import os, json
from pydantic import BaseModel, ValidationError, Field
from enum import Enum

CONFIG_DIR = "./src/configuration/conf"
USER_CONFIG = "./src/configuration/conf/user.json"
USER_CONFIG_BACKED = "./src/configuration/conf/user.backup.json"
CONFIG = {
  "user": {
    "joiningDate": None,
    "onboardingStatus": True,
    "genderIdentity": "prefer_not_to_say", 
    "name": {
      "firstName": "user",
      "lastName": None
    },
  }
}


class GenderIdentity(str, Enum):
    male = "male"
    female = "female"
    transgender = "transgender"
    nonbinary = "nonbinary"
    agender = "agender"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"

class Name(BaseModel):
    firstName: str = Field(default="user")
    lastName: str | None 

    class Config:
        extra = "forbid" # no extra option

class User(BaseModel):
    joiningDate: str | None
    onboardingStatus: bool 
    genderIdentity: GenderIdentity
    name: Name


    class Config:
        title = "config option"
        description = "A model for verfying config"
        extra = "forbid" # no extra option

user_data = User(**CONFIG["user"])


def ensure_config_directory():
    """
    genrate config if not present
    """
    if not os.path.exists(CONFIG_DIR):
        print("genrating missing config directory")
        os.mkdir(CONFIG_DIR)
        print("directory is genrated")
    else:
        print("configuration directory located sucessfully")


def ensure_user_config_exists():
    """
    genrate user config if not there
    """
    if not os.path.exists(USER_CONFIG):
        print("missing user configuration")
        _genrate_user_configuration()
    else:
        print("found existing user configuration file")


def _genrate_user_configuration():
    """
    genraing config based on pydantic model 
    """
    print("genrating user configuration...")
    with open(USER_CONFIG, "w") as user_file:
        user_file.write(user_data.model_dump_json(indent=2))


def _is_valid_json():
    """
    check if user config is valid json
    """
    try:
        with open(USER_CONFIG, "r") as user_file:
            json.load(user_file)
            print("valid json found")
            return True

    except (json.JSONDecodeError, FileNotFoundError) :
        print("invalid json")
        return False

def _is_valid_config_schema():
    """
    check if user config match pydantic BaseModel
    """
    with open(USER_CONFIG, "r") as user_file:
        user_data = json.load(user_file)
        try:
            _validate = User(**user_data)
            print("config match valid schema")
            return True

        except ValidationError as e:
            print("invalid config option Validation Error:", e)
            return False


def fix_user_config():
    print("fixing config file...")
    backup_user_config()
    print("removing bad config file...")
    _genrate_user_configuration()


def backup_user_config(): 
    with open(USER_CONFIG, "r") as user_file:
        content = user_file.read()
    with open(USER_CONFIG_BACKED, "w") as user_backup_file:
        user_backup_file.write(content)
    print(f"file content is backed up at {USER_CONFIG_BACKED}")


def handle_config():
    """
    handle everything related config
    """
    print("\n\nlocating config...")
    ensure_config_directory()
    ensure_user_config_exists()
    print("loading the config...")

    json_status = _is_valid_json()
    schema_status = _is_valid_config_schema()
    print("json status",json_status,"and schema status", schema_status)

    if not (json_status and schema_status):
        fix_user_config()
        handle_config()
    else:
        print("all set..")



def get_option():
    """
    get set options from config
    """
    with open(USER_CONFIG, "r") as user_file:
        user_data = json.load(user_file)
        data = User(**user_data)
        return data


def update_config(new_user_data):
    """
    updata config based on pydantic model
    """
    print("updating user configuration...")
    with open(USER_CONFIG, "w") as user_file:
        user_file.write(new_user_data.model_dump_json(indent=2))
