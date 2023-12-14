# Forklift Change Log
All notable changes to this project will be documented in this file.


## [0.2.6] - 2023-12-14
#### Added
- Standalone, self contained single file application is now ready. If you
  don't want to clone or copy the whole project just take `forklift.app`
  with you on your favorite local or remote host.  
  Self-contained standalone still requires: python, python-curses.  
  This is a fully working minified python application ready to run.
#### Changed
- Finally removed yaml library dependency from this project. The only
  dependency is now the curses library, there's no need for a virtualenv.
#### To Do
- pypi version it's still on testing phase and hatchling need few tweaks,
  please use github repo version at the moment
---


## [0.2.5] - 2023-12-12
#### Added
- Removed `system.yaml` configuration file completely, there's no need of
  a oneliner config file anymore. Container engine now detected on startup.
#### To Do
- Self contained single file application is now under testing, it will be
  available from the next release
- pypi version it's still on testing phase and hatchling need few tweaks,
  please use github repo version at the moment
- testunits for CLI and widgets, how to ?
---


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
