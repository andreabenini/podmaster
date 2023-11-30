# systempodctl

#### Containers and programs as systemd services made easy.
This is a simple utility for creating systemd services on the fly.
It's a matter of fact you sometimes need to create services from really simple projects
for small daily tasks. Being an SRE makes you think about automation all the time and
this utility creates identical services for containers, small python daemons and utilities
I manage every day.  
You can still create service files on your own but `systempodctl` can complete basic tasks
in seconds instead of minutes.  
This is not a replacement of systemd utilities and it's just a small `.service` files generator.

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

### Prerequisites
- It's a python program, `python3` needs to be installed. No virtualenv, packages or additional
libraries are required.
- This is a small utility without pretensions, mainly an helper for creating systemd
service files quickly. Virtualenv or fancy modules are not required at all.
There's no need to install it through pip and you can barely get it by cloning this repository only.

### Installation
- Clone this repository (`git clone http://..`)
- Save `systempodctl` utility wherever you prefer, it might be better if reachable from your
local `$PATH` variable
- ~~Through `pip install podmaster`~~.  
_Pypi.org account and project setup completed. Test in progress but it's **not yet ready for prime time**_



## Usage
**`systempodctl --help`**
```txt
usage: systempodctl [-h] [-t TYPE] [-n NAME] [-p PATH] command

systemdpodctl: manage unit-files for containers and standalone programs

positional arguments:
  command               types: (list-unit-files, edit, delete, journal)
                        list-unit-files.  Display units created with this utility
                        edit.             Create/Edit systemd service for python|container
                        delete.           Delete a systempodctl created service
                        journal.          Open journal and report logs in follow mode for --name

options:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  Service type (python,container)
  -n NAME, --name NAME  Service name
  -p PATH, --path PATH  Absolute path used when creating a service (Default:./)
                        ALWAYS use an absolute path

[NOTE] Services will be created with current user privileges unless otherwise specified.
       Please use <sudo> to create root services able to run without being logged in.
```
```sh
# List existing services (system and user services with 'systempod*' pattern)
systempodctl list-unit-files

# Create/Edit a python program based service
systempodctl edit --type python --name yourservicename --path /python/program/full/path
# Create/Edit a container based service (podman/docker)
systempodctl edit --type container --name yourservicename --path /container/full/path/dir

# Delete a previously created service (from this utility)
systempodctl delete --name yourservicename

# Provide journald log capabilities on stdout, useful for debugging, same as:
#     journalctl --unit yourservicename [--user] --follow
# for 'yourservicename' the leading 'systempod.' part is totally optional and autodetected
# from the utility if needed, so basically these two commands are the same:
systempodctl --name yourservicename journal
systempodctl --name systempod.yourservicename journal
```

## Features
- Handy `.service` files generator
- Few basic information required for creating a new service: ServiceName, working path
- Generate service files for your python daemons, virtualenv fully supported when needed
- Generate service files for containers, builtin template provide insights and guidance
through various dependencies and common issues when dealing with docker or podman

## Contributing
- On: https://github.com/andreabenini/podmaster use builtin project capabilities to
submit: hints, issues, bugs or whatever you prefer to solve your tasks
- Feel free to submit MergeRequests or review code in case you need it
- Contact the Author for further requests

## License
This project is licensed under the **[Affero GPLv3]** - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
This is not part of systemd CLI standard utilities and just a companion to them.
