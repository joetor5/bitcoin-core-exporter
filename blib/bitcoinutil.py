# Copyright (c) 2024 Joel Torres
# Distributed under the MIT software license, see the accompanying
# file LICENSE or https://opensource.org/license/mit.

import os
import platform
from pathlib import Path


if platform.system() == "Linux":
    BITCOIN_DIR = Path.joinpath(Path.home(), ".bitcoin")
elif platform.system() == "Darwin":
    BITCOIN_DIR = Path.joinpath(Path.home(), "Library", "Application Support", "Bitcoin")

class BitcoinConfigError(Exception):
    pass

def load_bitcoin_config(config_path: Path = BITCOIN_DIR) -> dict:
    config_file = Path.joinpath(config_path, "bitcoin.conf")
    config = {}
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                if line.startswith("#"):
                    continue

                if "=" in line:
                    equal_pos = line.find("=")
                    key = line[:equal_pos]
                    val = line[equal_pos+1:]
                    config[key] = val.strip()

    return config

def get_bitcoin_rpc_credentials(bitcoin_config: Path = BITCOIN_DIR, custom_config: dict = None) -> tuple:
    # get from env variables
    rpc_user = os.getenv("BITCOIN_RPC_USER")
    rpc_password = os.getenv("BITCOIN_RPC_PASSWORD")
    if rpc_user and rpc_password:
        return rpc_user, rpc_password

    # get from bitcoin.conf
    config = load_bitcoin_config(bitcoin_config)
    if config:
        if "rpcuser" in config and "rpcpassword" in config:
            return config["rpcuser"], config["rpcpassword"]

    # get from custom config
    if custom_config:
        rpc_user = custom_config.get("rpc_user", "")
        rpc_password = custom_config.get("rpc_password", "")
        if rpc_user and rpc_password:
            return rpc_user, rpc_password
    
    raise BitcoinConfigError("Unable to get bitcoin rpc credentials")

