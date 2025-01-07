import os, json

CONFIG_DIR = "./src/configuration/conf"
DEFAULT_CONFIG = "./src/configuration/conf/default.json"
USER_CONFIG = "./src/configuration/conf/user.json"
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


def ensure_default_config():
    with open(DEFAULT_CONFIG, "w") as file:
        json.dump(CONFIG, file, indent=4)
    print("fresh default config genrated")

def ensure_user_config():
    with open(USER_CONFIG, "w") as file:
        json.dump(CONFIG, file, indent=4)
    print("user config is overrited")


def handle_config():
    """
    handle everything related config
    """
    print("loading the config...")
    ensure_config_directory()
    





def genrate_new_config():
    """
    check if ./conf/default.conf and ./conf/user.conf exist or not
    genrate fresh new  ./conf/default.conf 
    if user.conf exist dont overrite
    if dose not exist copy from ./conf/default.conf
    """
    pass

def fix_conf():
    """
    if config has invalid data 
    move content to of .config/user.config to user.backup.conf
    copy ./conf/default.conf to ./conf/user.conf
    """
    pass
