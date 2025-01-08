import os, json
from datetime import datetime 
from pydantic import BaseModel 

CONFIG_DIR = "./src/configuration/conf"
USER_CONFIG = "./src/configuration/conf/user.json"
USER_CONFIG_BACKED = "./src/configuration/conf/user.backup.json"
CONFIG = {
  "user": {
    "joiningDate": None,
    "onboardingStatus": True,
    "name": {
      "firstName": "user",
      "lastName": None
    },
  }
}


class Name(BaseModel):
    firstName: str 
    lastName: str | None 


class User(BaseModel):
    joiningDate: datetime | None
    onboardingStatus: bool 
    name: Name

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
        genrate_user_configuration()
    else:
        print("found existing user configuration file")


def genrate_user_configuration():
    """
    genraing config based on pydantic model 
    """
    print("genrating user configuration...")
    with open(USER_CONFIG, "w") as user_file:
        user_file.write(user_data.model_dump_json(indent=2))

def load_user_config():
    """
    is user config is valid json 
    """
    try:
        with open(USER_CONFIG, "r") as user_file:
            json.load(user_file)
            print("valid json found")
        return True

    except (json.JSONDecodeError, FileNotFoundError) :
        print("invalid json")
        return False  


def validate_user_config():
    ...


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
    print("loading the config...")
    ensure_config_directory()
    ensure_user_config_exists()
    print("---------------------------")

    load_user_config()
