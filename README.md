# clip: CLI Project

This is really just a command wrapper around various commands to run
at a project root level.

Originally it was to build/debug/run c++ stuff from an editor
(emacs!), but there's no reason it should be tied to c++ or emacs.

Maybe it's more necessary for c++ since there's a lack of standard
tooling.  In some sense, this project is inspired by rust's cargo
tool.

# Intended Audience

Vim and Emacs support `:make` / `M-x compile` but those are rarely used to
build a project.  The intent is to provide a cli tool that runs some
high level commands on a project basis that can be easily used from
various editors.  The configuration file to capture these commands can
be persisted with the source.

# Config File

Here's a sample configuration file using meson/ninja (apologies for
the comments, `clip` strips those out).  This would be placed at the
root of a project as `.clip.json`.

```json
{
    // parameters that will build this project
    "build": {
        // Various "profiles"
        "release": {
            "command": "ninja -j@NUM_CORES_TO_USE@'",
            "working_dir": "build"
        },
        "debug": {
            "command": "ninja -j@NUM_CORES_TO_USE@'",
            "working_dir": "build-debug"
        },
        "cross": {
            "command": "ninja -j@NUM_CORES_TO_USE@'",
            "working_dir": "build-cross"
        },
        "test": {
            // Can set environment variables when running profiles
            "env": {
                "BOOST_TESTS_TO_RUN": "subset"
            },
            "command": "ninja test",
            "working_dir": "build-debug"
        }
    },

    // run the "tests" binary with gdb in the "build-debug" directory
    "debug": {
        "program": "tests",
        "working_dir": "build-debug",

        "program_args": ""

        // "env" also supported here
    },

    // Process compile_commands.json file[s] in various ways to
    // generate a new one to stdout
    "compile-commands": {
        "working_dir": "build-debug",
        //"ignore_args": "args to ignore",
        //"override_compiler": true

        // Filter compile_commands.json
        // {directory_,command_,file_}filter_regexes
        // "filter_regexes": {
        //     "regex": "replacement"
        // }

        // You can specify more than one file that will get merged into one
        "files": [
            "compile_commands.json",
            "compile_commands2.json"
        ]

    }
}
```

`NUM_CORES_TO_USE` is referenced from the environment in order to cap
parallel jobs to be less than cores+1.  Otherwise a machine can be
brought to it's knees...

## Compile Commands

Support was added to this tool in order to cater to the `cquery` c++
language server.  It was easier to provide a script that combined
compile_commands.json than it was to teach `cquery` to read multiple
files.  The regex stuff was added to take compile databases from cross
compiled builds and still run them through `cquery`.

# Usage

```
./clip <sub command> <sub command arguments>

 Sub commands:

  build [profile]
  debug
  generate-compile-db <directory>
```

# TODO

* `clip build --target=profile` instead of `clip build profile`
* tests?
* more flexible json schema for handling debugging targets and tests
* better schema?
* give this script some python "love"
  * setup.py?
  * better module layout?
