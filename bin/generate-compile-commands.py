#!/usr/bin/env python3

"""Modify compile_commands.json for cquery depending on emacsproject config"""

# Don't complain about dashes in script name, I like them better than underscores
# pylint: disable=locally-disabled, invalid-name

import json
import os
import sys
import emacsproject.config
import re

def perform_substitutions(line, regex_map):
    """Generic function to exercise a bunch of regexes on some text"""

    for regex, new_text in regex_map.items():
        line = re.sub(regex, new_text, line)

    return line

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

    # Process some filter regexes
    filter_regexes = config['cquery'].get('filter_regexes', {})
    directory_filter_regexes = config['cquery'].get('directory_filter_regexes', {})
    command_filter_regexes = config['cquery'].get('command_filter_regexes', {})
    file_filter_regexes = config['cquery'].get('file_filter_regexes', {})

    with open(os.path.join(project_dir, working_dir, 'compile_commands.json')) as descriptor:

        commands_db = json.load(descriptor)

        for entry in commands_db:

            # Perform all filter regexs
            for i in ['directory', 'command', 'file']:
                entry[i] = perform_substitutions(entry[i], filter_regexes)

            entry['directory'] = perform_substitutions(entry['directory'], directory_filter_regexes)
            entry['command'] = perform_substitutions(entry['command'], command_filter_regexes)
            entry['file'] = perform_substitutions(entry['file'], file_filter_regexes)

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
