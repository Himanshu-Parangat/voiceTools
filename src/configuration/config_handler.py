import os, json

CONFIG_DIR = "./src/configuration/conf"
DEFAULT_CONFIG = "./src/configuration/conf/default.json"
USER_CONFIG = "./src/configuration/conf/user.json"
USER_CONFIG_BACKED = "./src/configuration/conf/user.backup.json"
CONFIG = [
  {
    "user": {
      "joiningDate": "",
      "onboardingStatus": "",
      "name": {
        "firstName": "",
        "lastName": ""
      }
    }
  }
]


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


def ensure_default_config():
    """
    regenerate default config
    """
    with open(DEFAULT_CONFIG, "w") as file:
        json.dump(CONFIG, file, indent=2)
    print("fresh default config genrated")

def ensure_user_config():
    """
    genrate user config if not there
    """
    if not os.path.exists(USER_CONFIG):
        print("missing user configuration")
        print("loading default configuration")
        with open(DEFAULT_CONFIG, "r") as default_file:
            default_data = json.load(default_file)
        print("copying default configuration to user configuration")
        with open(USER_CONFIG, "w") as user_file:
            json.dump(default_data, user_file, indent=2)


def load_user_config():
    try:
        with open(USER_CONFIG, "r") as user_file:
            user_data = json.load(user_file)
            return user_data
    except json.JSONDecodeError as e:
        print(f"Error: The user configuration file '{USER_CONFIG}' contains invalid JSON. Details: {e}")
        backup_user_config()
        raise e

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
    ensure_default_config()
    ensure_user_config()
