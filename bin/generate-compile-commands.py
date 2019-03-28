#!/usr/bin/env python3

"""Generate compile_commands.json depending on emacsproject config"""

# Don't complain about dashes in script name, I like them better than underscores
# pylint: disable=locally-disabled, invalid-name

import json
import os
import sys
import re
import emacsproject.config


def perform_substitutions(line, regex_map):
    """Generic function to exercise a bunch of regexes on some text"""

    for regex, new_text in regex_map.items():
        line = re.sub(regex, new_text, line)

    return line


def main():
    """main"""

    project_dir = sys.argv[1]
    config_file = project_dir + os.sep + emacsproject.config.FILENAME

    if not os.path.exists(config_file):
        print("ERROR: unable to locate emacs project config file: " + config_file)
        sys.exit(1)

    # Try to read config file
    config = emacsproject.config.load_json_file(config_file)

    # get values (with some fallback defaults)
    working_dir = config['compile-commands'].get('working_dir', 'build')
    override_compiler = config['compile-commands'].get('override_compiler', False)
    ignore_args = config['compile-commands'].get('ignore_args', '').split()

    # Process some filter regexes
    filter_regexes = config['compile-commands'].get('filter_regexes', {})
    directory_filter_regexes = config['compile-commands'].get('directory_filter_regexes', {})
    command_filter_regexes = config['compile-commands'].get('command_filter_regexes', {})
    file_filter_regexes = config['compile-commands'].get('file_filter_regexes', {})

    # Default if not set in config file
    compile_commands_files = config['compile-commands'].get('files', ['compile_commands.json'])

    complete_commands_db = []

    for compile_commands_file in compile_commands_files:

        # TODO: take a list of files and concatenate them together
        with open(os.path.join(project_dir, working_dir, compile_commands_file)) as descriptor:

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

                complete_commands_db.append(entry)

    json.dump(complete_commands_db, sys.stdout)


if __name__ == "__main__":
    main()
