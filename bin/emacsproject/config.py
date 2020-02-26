r"""Configuration Helpers for emacs project

mainly to load json config file
"""

import os
import os.path
import json

FILENAME = ".emacs_project.json"
DEBUG = False


def remove_comments(text):
    """Remove comments from json string

    Since officially, json doesn't contain comments
    """

    ret = ""
    count = 0
    for line in text.split("\n"):
        if not line.lstrip().startswith("//"):
            ret += line + "\n"
            if DEBUG:
                print(str(count) + ":" + line)
            count += 1
    return ret


def load_json_file(json_file):
    """Read json file"""

    json_text = open(json_file).read()
    return json.loads(remove_comments(json_text))


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
