#!/usr/bin/env python3

import json
import os
import sys

# TODO: consolidate these helper functions

def removeComments(text):
    ret = ""
    count = 0
    for line in text.split("\n"):
        if not line.lstrip().startswith("//"):
            ret += line + "\n"
            #print str(count) + ":" + line
            count += 1
    return ret

def loadJsonFile(filename):
    # Read config file
    json_text = open(filename).read()
    return json.loads(removeComments(json_text))

project_dir = sys.argv[1]
cquery_config_file = project_dir + os.sep + ".emacs_project.json"

# Try to read config file
config = loadJsonFile(cquery_config_file)

# get values (with some fallback defaults)
working_dir       = config['cquery'].get('working_dir', 'build')
override_compiler = config['cquery'].get('override_compiler', False)
ignore_args       = config['cquery'].get('ignore_args', '').split()

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
