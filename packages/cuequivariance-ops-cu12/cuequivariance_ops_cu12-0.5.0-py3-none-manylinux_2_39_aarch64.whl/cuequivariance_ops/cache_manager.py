# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import hashlib
import json
import math
import os
from typing import Any

import pynvml
import torch


def get_gpu_information():
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available")
    current_device = torch.cuda.current_device()
    props = torch.cuda.get_device_properties(current_device)

    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(current_device)
    power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(handle)
    max_clock_rate = pynvml.nvmlDeviceGetMaxClockInfo(
        handle, pynvml.NVML_CLOCK_GRAPHICS
    )
    pynvml.nvmlShutdown()

    return {
        "name": props.name,
        "total_memory": math.ceil(props.total_memory / (1024**3)),
        "multi_processor_count": props.multi_processor_count,
        "power_limit": power_limit // 1000,
        "clock_rate": max_clock_rate,
        "major": props.major,
        "minor": props.minor,
    }


def gpu_information_to_key(information: dict) -> str:
    information.pop("name", None)
    key_string = "_".join(f"{value}" for value in information.values()).replace(
        " ", "_"
    )
    hash_object = hashlib.sha256(key_string.encode())
    hast_str = hash_object.hexdigest()
    return hast_str


class CacheManager:
    """Singleton managing the cache"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
            cls._instance.gpu_information = get_gpu_information()
            cls._instance.gpu_key = gpu_information_to_key(
                cls._instance.gpu_information
            )
        return cls._instance

    def load_cache(
        self, fn_key: str, json_path: str = os.path.dirname(__file__)
    ) -> dict:
        # load the json file and store it in the cache-dict
        json_file = os.path.join(json_path, f"{fn_key}.json")
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                fn_cache = json.load(f)
                self.cache[fn_key] = fn_cache
        else:
            # if the file does not exist, create an empty dict for the specified function
            fn_cache = self.cache[fn_key] = {}

        return fn_cache

    def save_cache(
        self, fn_key: str, json_path: str = os.path.dirname(__file__)
    ) -> None:
        # save cache-dict to json file
        json_file = os.path.join(json_path, f"{fn_key}.json")
        # Load existing data from the file if it exists
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = {}

        # Merge the existing data with the current cache
        merged_data = {**existing_data, **self.cache[fn_key]}

        # Save the merged data back to the file
        with open(json_file, "w") as f:
            json.dump(merged_data, f, indent=4)

        # Update the cache with the merged data
        self.cache[fn_key] = merged_data

    def get(
        self, fn_key: str, inp_key: str, json_path: str = os.path.dirname(__file__)
    ) -> Any:
        # get value from cache
        # if necessary, load json first
        fn_cache = (
            self.load_cache(fn_key) if fn_key not in self.cache else self.cache[fn_key]
        )
        # check if fn_key and inp_key exist in cache
        if self.gpu_key in fn_cache and inp_key in fn_cache[self.gpu_key]:
            return self.cache[fn_key][self.gpu_key][inp_key]
        else:
            # if not found, return None or raise an error
            return None

    def set(self, fn_key: str, inp_key: str, value: Any) -> None:
        # write value to cache-dict
        # and write-back to json
        if fn_key not in self.cache:
            self.cache[fn_key] = {}
        if self.gpu_key not in self.cache[fn_key]:
            self.cache[fn_key][self.gpu_key] = {"gpu_information": self.gpu_information}
        self.cache[fn_key][self.gpu_key][inp_key] = value
