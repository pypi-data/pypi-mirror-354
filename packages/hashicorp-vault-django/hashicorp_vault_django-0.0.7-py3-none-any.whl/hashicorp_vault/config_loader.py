import os
import yaml


def load_config(base_dir):
    """
    Load YAML configuration from the first .yml file found inside the config or env_config directory.
    If no .yml file is found, load from a default file named 'env_config.yml'.
    """
    config_dirs = ['config/']

    for config_dir in config_dirs:
        dir_path = os.path.join(base_dir, config_dir)
        config_file = os.path.join(dir_path, 'application.yml')
        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            return config
        else:
            if os.path.exists(dir_path):
                files = [file for file in os.listdir(dir_path) if file.endswith('.yml')]
                if files:
                    config_file = os.path.join(dir_path, files[0])
                    with open(config_file, 'r') as file:
                        config = yaml.safe_load(file)
                    return config
    return None
