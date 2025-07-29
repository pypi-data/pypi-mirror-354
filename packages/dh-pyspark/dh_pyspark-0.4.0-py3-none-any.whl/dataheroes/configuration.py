import os
import re
from pathlib import Path
import configparser


def get_library_code():
    return 'dataheroes'

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            # if instance already exists
            # and for inherited class method add_params is defined,
            #  run it instead the constructor
            if getattr(cls._instances[cls], 'add_params', None):
                cls._instances[cls].add_params(*args, **kwargs)
        return cls._instances[cls]


def get_config_license_key():
    return DataHeroesConfiguration().get_param_str("license_key")


def _parse_file(path):
    """
    return config from path as list [{"section": ..., "name", ..., "value": ...}, ...]
    """
    if os.path.exists(path):
        config = configparser.ConfigParser()
        config.read(path)
        items = []
        for section in config.sections():
            for item in config.items(section):
                items.append({"section": section, "name": item[0], "value": item[1]})
        return items
    return []


def _parse_dict(config: dict):
    items = []
    for section in config:
        for item in config[section]:
            items.append({"section": section, "name": item, "value": config[section][item]})
    return items


class DataHeroesConfiguration(metaclass=Singleton):
    """
        + class DataHeroesConfiguration(license_key="val1", ....) to set config params
        + function to get params DataHeroesConfiguration().get_param(param_name="license_key", section=None)
        + config file
            [licensing]
                license_key=<Your license key>
            [telemetry]
                exporter_type_https=0/1
            [misc]
                working_directory=...
                cache_dir=...
                dir_path=...
        + prioritizes setting configuration parameters in the following order:
            Arguments passed to the DataHeroesConfiguration object
            params as dict passed to the DataHeroesConfiguration
            Environment parameters, for example, DATAHEROES_LICENSE_KEY=<Param Value>
            A setting in the .dataheroes.config file on path in env variable DATAHEROES_CONFIG_PATH
            A setting in the .dataheroes.config file in your current folder
            A setting in the .dataheroes.config file in your HOME directory
    """

    def __init__(self, config_file_path: str = None, config_dict: dict = None, **config_params):
        # dict with params of DataHeroesConfiguration init = {"license_key": ..., "working_directory": ....}
        self.init_params = config_params
        self.init_config_dict = config_dict or {}
        self.config_as_list = []
        self.config_file_path = config_file_path
        self.build_configs(config_dict=config_dict, **config_params)

    def build_configs(self, config_dict: dict = None, **config_params):
        """
        build self.config_as_list, in order of priorities of sources
        duplicates are possible and acceptable, if certain param exists more that in one sources,
        it should be met self.config_as_list more that once.
        """
        self.init_params.update(config_params)
        if config_dict:
            self.init_config_dict.update(config_dict)
        config_file_name = f'.{get_library_code()}.config'
        config_path_env_name = f'{get_library_code()}_CONFIG_PATH'.upper()
        self.config_as_list = []
        real_config_file_path = None
        if self.config_file_path:
            real_config_file_path = self.config_file_path
        elif config_path_env_name in os.environ:
            real_config_file_path = os.environ[config_path_env_name]

        def append_param(param_full_name, param_value):
            env_split = param_full_name.split('__')
            if len(env_split) > 1:
                section_name = env_split[0]
                param_name = env_split[1]
            else:
                section_name = "default"
                param_name = env_split[0]

            self.config_as_list.append({
                "section": section_name,
                "name": param_name,
                "value": param_value
            })

        for (prm_name, prm_value) in [(prm_name, self.init_params[prm_name]) for prm_name in self.init_params]:
            append_param(prm_name, prm_value)

        if self.init_config_dict:
            self.config_as_list += _parse_dict(self.init_config_dict)

        for (prm_name, prm_value) in [(env_name.lstrip(f'{get_library_code()}_'.upper()).lower(), os.environ[env_name])
                                      for env_name in os.environ if env_name.startswith(f'{get_library_code()}_'.upper())]:
            append_param(prm_name, prm_value)

        if real_config_file_path and Path(real_config_file_path).is_file():
            self.config_as_list += _parse_file(real_config_file_path)
        elif real_config_file_path:
            self.config_as_list += _parse_file(os.path.join(real_config_file_path, config_file_name))

        self.config_as_list += _parse_file(os.path.join(os.getcwd(), config_file_name))
        self.config_as_list += _parse_file(os.path.join(str(Path.home()), config_file_name))

    def add_params(self, config_file_path: str = None, config_dict: dict = None, **config_params):
        """
        add/update params without destroying existing
        """
        self.init_params.update(config_params)
        self.build_configs(config_dict=config_dict)
        if config_file_path:
            self.config_file_path = config_file_path

    def save_to_file(self, path):
        """
        Save config to file
        """
        last_section = ''
        last_name = ''
        with open(path, 'w') as config_file:
            for item in sorted(self.config_as_list, key=lambda x: x.get('section', 'default_')+x.get('name')):
                if item.get('name') != last_name:
                    # no duplicates allowed! and first value is correct (has top priority)
                    current_section = item.get('section', 'default')
                    if current_section != last_section:
                        config_file.write(f'[{current_section}]\n')
                    last_section = current_section
                    config_file.write(f'  {item.get("name")}={item.get("value")}\n')
                last_name = item.get('name')

    @staticmethod
    def _update_create_config_file_by_name(file_path, section_name, param_name, param_value):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
        else:
            lines = []
        found_param = False
        with open(file_path, 'w') as file:
            for line in lines:
                if not found_param and re.match(r"^\s*{}".format(re.escape(param_name + '=')), line):
                    line = line.replace(line.split('=')[1], param_value + '\n')
                    found_param = True
                file.write(line)

        if not found_param:
            added_param = False
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line)
                    if not added_param and line.startswith(f'[{section_name}'):
                        file.write(f'\n')
                        file.write(f'    {param_name}={param_value}\n')
                        added_param = True

                if not added_param:
                    file.write(f'\n')
                    file.write(f'[{section_name}]\n')
                    file.write(f'    {param_name}={param_value}\n')

    @staticmethod
    def top_priority_file_path():
        config_file_name = f'.{get_library_code()}.config'
        config_path_env_name = f'{get_library_code()}_CONFIG_PATH'.upper()
        env_path_ver_1 = os.environ[config_path_env_name] if config_path_env_name in os.environ else ''
        env_path_ver_2 = os.path.join(os.environ[config_path_env_name], config_file_name) \
            if config_path_env_name in os.environ else ''
        current_folder_path = os.path.join(os.getcwd(), config_file_name)
        home_folder_path = os.path.join(str(Path.home()), config_file_name)

        if os.path.isfile(env_path_ver_1):
            return env_path_ver_1
        elif os.path.isfile(env_path_ver_1):
            return env_path_ver_2
        elif os.path.isfile(current_folder_path):
            return current_folder_path
        else:
            return home_folder_path

    def update_create_config_file(self, section_name, param_name, param_value):
        """
        if exists config file
            if exists param - update value (for first occurrence)
            else add param_pame=param_value into new [section_name]
        else (file not exists)
            create config file in HOME dir and such param
        """
        self._update_create_config_file_by_name(
            file_path=DataHeroesConfiguration.top_priority_file_path(),
            section_name=section_name,
            param_name=param_name,
            param_value=param_value
        )

    def get_param(self, name, section=None, default_value=None):
        # init params have top priority
        for item in self.config_as_list:
            if ((section is None) or (item.get("section") == section)) and item.get("name") == name:
                return item.get("value")
        return default_value

    def get_param_str(self, name, section=None, default_value=None):
        result = self.get_param(name, section, default_value)
        if result is not None:
            return str(result)
        return None

    def get_param_bool(self, name, section=None, default_value=None):
        result = self.get_param(name, section, default_value)
        if result is not None:
            return result.lower() not in ['0', 'false', 'f'] if isinstance(result, str) else bool(result)
        return None

    def get_param_int(self, name, section=None, default_value=None):
        result = self.get_param(name, section, default_value)
        if result is not None:
            return int(result)
        return None

    def get_param_float(self, name, section=None, default_value=None):
        result = self.get_param(name, section, default_value)
        if result is not None:
            return float(result)
        return None

    @classmethod
    def clear_instance(cls):
        if cls in cls._instances:
            del cls._instances[cls]
