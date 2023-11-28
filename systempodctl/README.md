# `NOTE:` this is basically a placeholder, code and doc will be plublished in the upcoming days

&nbsp;
---

# systempodctl

Managing containers and programs as systemd services made easy.

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
python3 needs to be installed, no virtualenv, packages or additional libraries are required.
This is almost a standalone utility, mainly an helper for creating systemd service files quickly.

### Installation
- Clone this repository
- Save `systempodctl` utility wherever you prefer, it might be better if reachable from $PATH variable



## Usage
```sh
# Usage help
systempodctl --help

# List existing services (system and user services)
systempodctl list-unit-files

# Create/Edit a python program based service
systempodctl edit --type python --name yourservicename --path /python/program/full/path
# Create/Edit a container based service (podman/docker)
systempodctl edit --type container --name yourservicename --path /container/full/path/dir

# Delete a previously created service
systempodctl delete --name yourservicename
```


## Features
~~Highlight key features of your project.~~
~~- todo List~~

## Contributing
Explain how others can contribute to your project. Include guidelines for submitting pull requests and reporting issues.

## License
This project is licensed under the [Affero GPLv3] - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
~~Mention and give credit to any third-party libraries, tools, or resources that you used or were inspired by.~~
