import json
import os


def load_config():
    path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
    config_file_path = os.path.join(path, "config.json")

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r', encoding="utf-8") as fp:
            config = json.load(fp)
        return True, config
    else:
        return False, None