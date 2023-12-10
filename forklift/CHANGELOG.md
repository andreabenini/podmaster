# Forklift Change Log
All notable changes to this project will be documented in this file.


## [0.2.4] - 2023-12-03
Bug fixing version, no new feature present
#### Added
- Output with success or failure messages on container images operations
- Text wrapping on widgets when output is too long
#### Changed
- Output operations on container images
- Displaying all images, even intermediate ones (labeled as '\<none\>')
#### Fixed
- Image removal errors were not properly reported to user
- Display tmp snapshots in images list (when present)
- Proper error management upon container deletion (when it's still running)
#### To Do
- pypi version still need some tweak, use github repo version instead
- testunits for CLI and widgets, how to ?
---


## [0.2.3] - 2023-12-01
First version published on Pypi, still in progress and needs to be fixed there..
#### Changed
- Version alignment from github repo as well as from Pypi packages.
  Release version, no bugfixing
---


## [0.2.0] - 2023-11-07
#### Added
- Versioning and documentation, license AGPL
- Project initially released on github
- Created as a python package and published on Python official repository.
    "`pip install forklift-container`" to have it installed
- container `logs` command added
#### Changed
- Configuration path as command line parameter
#### To Do
- python unittest on a curses widget, how to ?
---


## [0.1.0] - 2023-11-06
Officially started as a registered project for
[SUSE Hack Week '23](https://hackweek.opensuse.org/)
#### Added
- Registered to HackWeek '23 as:
[Forklift - Text based GUI utility for dealing with containers](https://hackweek.opensuse.org/23/projects/forklift-text-based-gui-utility-for-dealing-with-containers)
- Built from scratch on top of python+curses+yaml, no other deps
#### Changed
- curses as a base, widget built from scratch for this project only
#### Fixed
- Fixing curses bug on Textbox() class, reported to python standard library
    - cpython official library [issue](https://github.com/python/cpython/issues/111795)
    - cpython library [patch provided](https://github.com/python/cpython/pull/111796)
