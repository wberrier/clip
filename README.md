# clip

CLI Project

This is really just a command wrapper around various commands to run
at a project root level.

Originally it was to build/debug/run c++ stuff from an editor
(emacs!), but there's no reason it should be tied to c++ or emacs.

Maybe it's more necessary for c++ since there's a lack of standard
tooling.  In some sense, this project is inspired by rust's cargo
tool.

# Usage

```
./clip <sub command> <sub command arguments>

 Sub commands:

  build [profile]
  debug
  generate-compile-db <directory>
```
