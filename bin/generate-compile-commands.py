#!/usr/bin/env python3

"""Modify compile_commands.json for cquery depending on emacsproject config"""

# Don't complain about dashes in script name, I like them better than underscores
# pylint: disable=locally-disabled, invalid-name

import json
import os
import sys
import emacsproject.config

def main():
    """main"""

    project_dir = sys.argv[1]
    cquery_config_file = project_dir + os.sep + emacsproject.config.FILENAME

    # Try to read config file
    config = emacsproject.config.load_json_file(cquery_config_file)

    # get values (with some fallback defaults)
    working_dir = config['cquery'].get('working_dir', 'build')
    override_compiler = config['cquery'].get('override_compiler', False)
    ignore_args = config['cquery'].get('ignore_args', '').split()

    with open(os.path.join(project_dir, working_dir, 'compile_commands.json')) as descriptor:

        commands_db = json.load(descriptor)

        for entry in commands_db:
            command = entry['command']

            args = command.split()

            new_args = []

            # Sanitize compile_commands.json
            for arg in args:

                if override_compiler:
                    if arg.endswith("gcc"):
                        arg = "clang"
                    elif arg.endswith("g++"):
                        arg = "clang++"

                if arg in ignore_args:
                    arg = ""

                new_args.append(arg)

            entry['command'] = " ".join(new_args)

        json.dump(commands_db, sys.stdout)

if __name__ == "__main__":
    main()
