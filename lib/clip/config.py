r"""Configuration Helpers for clip

mainly to load json config file
"""

import os
import os.path
import json

FILENAME = ".clip.json"


def remove_comments(text, logger=None):
    """Remove comments from json string

    Since officially, json doesn't contain comments
    """

    ret = ""
    count = 0
    for line in text.split("\n"):
        if not line.lstrip().startswith("//"):
            ret += line + "\n"
            if logger:
                logger.debug(str(count) + ":" + line)
            count += 1
    return ret


def load_json_file(json_file, logger=None, replacements={}):
    """Read json file"""

    if logger:
        logger.info("Reading json file: " + json_file)
    json_text = open(json_file).read()

    for key, value in replacements.items():
        json_text = json_text.replace(key, value)

    return json.loads(remove_comments(json_text, logger))


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
