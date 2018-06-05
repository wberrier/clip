#!/usr/bin/env python3

import json
import os
import sys
import configparser

project_dir = sys.argv[1]
cquery_config_file = project_dir + os.sep + ".emacs_cquery.conf"

# Try to read config file
config = configparser.ConfigParser()
# set some defaults
config.add_section('config')
config.set('config', 'working_dir',       'build')
config.set('config', 'override_compiler', 'false')
config.set('config', 'ignore_args',       '')

if os.path.exists(cquery_config_file):
    config.read(cquery_config_file)

working_dir       = config.get       ('config', 'working_dir')
override_compiler = config.getboolean('config', 'override_compiler')
ignore_args       = config.get       ('config', 'ignore_args').split()

with open(os.path.join(project_dir, working_dir, 'compile_commands.json')) as f:

    db = json.load(f)

    for entry in db:
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

    json.dump(db, sys.stdout)
