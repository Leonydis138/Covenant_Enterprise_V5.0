import os
import json

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def save_config(path, config):
    with open(path, "w") as f:
        json.dump(config, f, indent=4)
