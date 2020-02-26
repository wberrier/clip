r"""Common helpers for clip
"""

import os


def print_environment(env):
    """Print environment"""

    for key, value in env.items():
        print("%s=%s" % (key, value))


def set_environment(env):
    """Set the environment according to a list of strings"""

    for key, value in env.items():
        os.environ[key] = value
