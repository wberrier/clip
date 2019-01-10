r"""Common helpers for emacs project
"""

import os

def set_environment(env_string):
    """Set the environment according to a string"""

    if ':' in env_string:
        key_values = env_string.split(':')
    else:
        key_values = (env_string,)

    for key_value in key_values:
        (key, value) = key_value.split('=')
        os.environ[key] = value
