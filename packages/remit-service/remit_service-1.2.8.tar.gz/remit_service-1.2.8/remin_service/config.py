import os
from pydantic import BaseModel, field_validator
from remin_service.helper import DataCent
from typing import Optional
from remin_service.helper.ip_helper import get_local_ip, get_public_ip

# data = DataCent.data


class ImportConfig:

    def __init__(self, config_key):
        self.__config_key__ = config_key
        self.__config__ = None
        self.__cls__ = None

    def __call__(self, cls):
        self.__cls__ = cls
        _config_keys = self.__config_key__.split(".")
        data = DataCent.data
        for _config_key in _config_keys:
            data = data.get(_config_key, {})
        return self

    def __getattr__(self, name):
        if name.startswith("_") or name.endswith("__"):
            return super().__getattribute__(name)
        if not self.__config__:
            _config_keys = self.__config_key__.split(".")
            data = DataCent.data
            for _config_key in _config_keys:
                # print(data)
                data = data.get(_config_key, {})
            self.__config__ = self.__cls__(**data)

        return self.__config__.__getattribute__(name)


@ImportConfig("config")
class Config(BaseModel):
    active: str


@ImportConfig("service")
class ServiceConfig(BaseModel):
    ip: str = ""
    ip_type: str = "local"
    port: int = 8080
    service_name: str = "service"

    def __init__(self, **kwargs):
        if "ip" not in kwargs:
            kwargs["ip"] = "0.0.0.0"
            kwargs["ip_type"] = "public"
        elif kwargs.get("ip") == "0.0.0.0":
            kwargs["ip_type"] = "local_public"
        super().__init__(**kwargs)

    @classmethod
    def get_ip(cls):
        if ServiceConfig.ip_type == "local_public":
            return get_local_ip()
        if ServiceConfig.ip_type == "local":
            return "127.0.0.1"
        if ServiceConfig.ip_type == "public":
            return get_public_ip()


@ImportConfig("cloud.nacos")
class NaNosConfig(BaseModel):
    class __Discovery(BaseModel):
        username: str = None
        password: str = None
        cluster_name: str = ""
        namespace: str = ""
        group: str = ""
        server_addr: str

    discovery: Optional[__Discovery] = None


# print(Config.active)

# print(Config.active)