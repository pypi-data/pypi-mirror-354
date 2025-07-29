import json
import os

def init_config():
    config = {
        "app_path": ".",
        "exclude": ["migrations", "__pycache__"],
        "docker_base": "python:3.10-slim"
    }

    with open("drf_protector.json", "w") as f:
        json.dump(config, f, indent=4)

    print("✅ Configuration initialized in drf_protector.json")
