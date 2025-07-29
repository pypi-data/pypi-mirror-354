import json
import os.path
from remin_service.helper import DataCent
import threading
import yaml


def env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    var_name = value.strip('${} ')
    vars = var_name.split(",")
    if len(vars) >= 3:
        raise Exception("Invalid variable name")

    if len(vars) == 1:
        return os.getenv(var_name, "")
    else:
        return os.environ.get(vars[0], vars[-1].strip('${} '))


def config_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    var_name = value.strip('${} ')
    result_dict = {}
    for pair in var_name.split(','):
        key, value = pair.split(':')
        if value in ['True', 'False']:
            result_dict[key] = value == 'True'
        elif value.isdigit():
            result_dict[key] = int(value)
        else:
            result_dict[key] = value
    return result_dict


yaml.FullLoader.add_constructor('!env', env_var_constructor)  # 为SafeLoader添加新的tag和构造器
yaml.FullLoader.add_constructor('!config', config_var_constructor)  # 为SafeLoader添加新的tag和构造器


def merge_dicts(*dicts):
    result = {}
    for d in dicts:
        for key, value in d.items():
            if isinstance(value, dict) and key in result:
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value
    return result


class ConfigLoad:

    _instance_lock = threading.Lock()

    @classmethod
    def instance(cls, config_path, service_path):
        with ConfigLoad._instance_lock:
            if not hasattr(ConfigLoad, "_instance"):
                ConfigLoad._instance = ConfigLoad(config_path, service_path)
        return ConfigLoad._instance

    def __init__(self, config_path, service_path):
        self.config_path = config_path
        self.service_path = service_path
        self.config_file = f"{self.config_path}/resources/config.yaml"

    def load(self):

        with open(self.config_file, encoding="utf8") as file:

            DataCent.data = merge_dicts(DataCent.data, yaml.load(file.read(), Loader=yaml.FullLoader) or {})

        active = DataCent.data.get("config", {}).get("active")
        if not active:
            return True

        include_config_file = f"""{self.config_path}\\resources\\config.{active}.yaml"""

        if not os.path.exists(include_config_file):
            raise FileNotFoundError(f"{include_config_file} 不存在")

        with open(include_config_file, encoding="utf8") as file:

            DataCent.data = merge_dicts(DataCent.data, yaml.load(file.read(), Loader=yaml.FullLoader) or {})

        include = DataCent.data.get("config", {}).get("include")

        if include.get("service"):
            include_service_config_file = f"""{self.service_path}\\resources\\config.{active}.yaml"""

            if not os.path.exists(include_service_config_file):
                return True

            with open(include_service_config_file, encoding="utf8") as file:

                DataCent.data = merge_dicts(DataCent.data, yaml.load(file.read(), Loader=yaml.FullLoader) or {})

        return True


if __name__ == '__main__':
    ConfigLoad.instance("/src/template/resources/config.yaml").load()