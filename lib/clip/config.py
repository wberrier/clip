r"""Configuration Helpers for clip

mainly to load config file
"""

import os
import os.path
import yaml

FILENAME = ".clip.yaml"


def load_file(config_file, logger=None, replacements={}):
    """Read config file"""

    if logger:
        logger.info("Reading config file: " + config_file)
    config_text = open(config_file).read()

    for key, value in replacements.items():
        config_text = config_text.replace(key, value)

    return yaml.safe_load(config_text)


def get_config_dir():
    """Get the directory that has the config file"""

    curdir = os.getcwd()
    while curdir != "/":

        test_file = curdir + "/" + FILENAME
        if os.path.exists(test_file):
            return curdir

        curdir = os.path.dirname(curdir)

    # Didn't find the config dir...
    return ""
