![Forklift logo](icon.png)

# Forklift - Text based utility for dealing with containers
### What is this for
This is a simple and handy text based GUI utility for dealing with boring
and repetitive tasks while managing containers.  
If you usually manage them in your daily activities you'll surely deal
a lot with the CLI and execute repetitive commands for: 
building images, creating containers, running, killing and stopping
them all the time.  

It doesn't really matter if you are a Developer, a DevOps or a SRE;
most of your time might be spent on the CLI for deleting/respawning/starting
new instances for your favorite product.  
You can surely do it from a GUI or editor (vscode, eclipse, ...)
but it might be messy if you're managing them remotely through SSH and 
all you have at your disposal is just your trusty text-only shell connection.  

That's the reason for this simple, quick, text-only curses based utility,
no matter if containers are running on a remote machine, locally or if you
prefer a specific Window Manager.
I expressly don't want to rely on X11/Wayland, infinite dependencies 
(or keep them to the bare minimum) and it has to be text-only and usable from
a remote shell.  
This utility relies on: python and curses bindings (just plain curses,
no extra widgets required).  
It is not a fully fledged solution but rather a small and quick tool for
running boring tasks, you'll still use docker/podman of your choice but you
don't want to be annoyed by usual and repetitive commands
    (`docker ps -a; docker kill <ID>; docker start <ID> <params, ...>`).
That's what this utility is about.


#### Rolling demo overview
https://github.com/andreabenini/podmaster/assets/9632086/198ac4c7-416a-4217-89c6-4eea30e46561


## Features 
- Basic container images management: create (manually/script), rename, delete
- Container management: create, run, attach, stop, kill, rename, log
- Running locally or on a remote SSH connection, text only, no GUI required
- Curses based GUI utility with just a few keys: cursor arrows, enter, escape
- **NOT** related to Kubernetes, orchestrators or pods, just "simple" containers.  
    Targeted to personal workstations and workflows, no matter if local or on a
    remote ssh shell
- python-curses is the only requirement, no extra deps, no curses library
    widgets. Everything builtin and self contained in the project
- _.yaml_ based user configuration
- Container engine independent, tested on: **_docker, podman_**. LXD might be the next
    if someone requires it
- Build images and container from within the utility, ContainerCommander like style


## Usage:
```sh
# program help
~$ forklift --help
usage: forklift [-h] [-p PATH]

Forklift: friendly utility for dealing with containers

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  System and user configuration files path (default: /where/this/utility/is/stored)

# As simple as:
~$ forklift
# Or add '--path' argument to specify where yaml config files are stored
#     default is set on program current location (see --help for details)
~$ forklift --path $HOME/container_configs
```
- Arrows keys to navigate
- \<enter> to confirm, \<esc> to abort commands


## Installation and configuration

- Requirements: _'python3'_ and _'python curses'_ are required, nothing else. There's **no need** for a VirtualEnv
- Installation methods:
    1. Download just `forklift.app` file and use it as a standalone application. Python and curses needs to be
    available in your system but nothing else is really needed. This compact executable contains everything,
    add optional .yaml files if you need them _(see below)_
    2. From source [the official repository](https://github.com/andreabenini/podmaster/tree/main/forklift),
    this site. Clone the repo or download sources from there
    3. ~~from **_pip_**~~: 
        ~~`pip install forklift/podmaster`~~
        **_(WORK IN PROGRESS, dealing the name with PyPi package maintainers)_**
- **_[Optional]_** Set `$EDITOR` environment variable in your favorite shell. If you have a working
    environment with *$EDITOR* set in place you can directly edit **`.yaml`** configuration files
    from the utility
    ```sh
    # file: $HOME/$USER/.bashrc
    # Default editor
    export EDITOR=/usr/bin/vim
    ```
- **_[Optional]_** Create your `containers.yaml` and `images.yaml` files to have working templates
    while using the utility. You can create and edit them externally from the shell or 
    automatically while using the program. These two samples are provided as a reference:
    `containers.yaml.sample`, `images.yaml.sample`. Future upgrades will never replace your working
    configuration.
    ```sh
    # optional, up to you, feel free to create or add info to yours
    cp containers.yaml.sample containers.yaml
    cp images.yaml.sample     images.yaml
    ```
- Start the program and you're ready to go, feel free to store it wherever you prefer
    ```sh
    ~$ forklift
    # ~$ forklift.app       # If you're using the minified version
    ```


## Contributing
Feel free to raise issues, pull requests and suggest improvements. It's a ready
made utility but it can be enhanced and new features might be added with your
contribution.
