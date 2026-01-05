import warnings
from typing import Tuple

import httpx
import os
import json
import tempfile
import time
from importlib.metadata import version as pkg_version

PACKAGE_NAME = "anicli_api"


def get_pypi_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = httpx.get(url)
    if response.status_code == 200:
        return response.json()["info"]["version"]
    return None


def get_cached_version(package_name):
    cache_file = os.path.join(tempfile.gettempdir(), f"{package_name}_version.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            data = json.load(f)
            timestamp = data.get("timestamp", 0)
            if time.time() - timestamp < 86400:
                return data.get("version"), timestamp
    return None, None


def save_cached_version(package_name, version):
    cache_file = os.path.join(tempfile.gettempdir(), f"{package_name}_version.json")
    with open(cache_file, "w") as f:
        json.dump({"version": version, "timestamp": time.time()}, f)


def check_version(package_name=PACKAGE_NAME):
    """ Doesn't work correctly on termux
    """
    
