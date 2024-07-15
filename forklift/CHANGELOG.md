# Forklift Change Log
All notable changes to this project will be documented in this file.


## [1.0.3] - 2024-07-15 [*Cthulhu*] LTS
Handy storage information at your disposal
#### Added
- [ System ] Menu. adding option: _"Storage Information"_ for displaying
  local disk storage information _(space is not infinite)_.
---


## [1.0.2] - 2024-02-27 [*Cthulhu*] LTS
Start/Attach commands auto detection on containers.
#### Added
- [ Inspect ]  container command to detect running options and arguments
  passed to a running container. Piping to less for comfortable reading.
---


## [1.0.1] - 2023-12-28 [*Cthulhu*] LTS
Start/Attach commands auto detection on containers.
#### Added
- [ Start - Attach ] container command now detects the running status and
  uses _start -ai_ or _exec -it_ accordingly.
- Shell  auto detection on container _Attach_ action, there is no need to
  execute a manual command for it (but still available just in case).
  Possible shell list from container class as an attribute.
#### Changed
- Start/Attach container action, different commands run based on status
---


## [1.0.0] - 2023-12-28 [*Cthulhu*] LTS
First stable LTS version.
#### Added
- New custom action on Container Menu for attaching demonized containers
  or executing custom commands on them.
#### Changed
- Auto adapting windows on containers/images creation
#### Fixed
- Extensive testing for a month, no problems emerged ever since, marking
  this version as the first available stable LTS version.
#### To Do
- pypi version it's still on testing phase and hatchling need few tweaks,
  please use github repo version at the moment. Still a WiP because I'm
  simply focusing on releasing just a single executable, this will be the
  final step before v1.0
- future releases in the 0.x branch will be considered as bugfixes, first
  stable will be labeled as 1.x
---


## [0.5.1] - 2023-12-28 [*Byakhee*]
Pre-release before first stable LTS, no extra features, bug fixing only.
#### Added
- This is a python3 program only, the interpreter is still needed even if
  I'm also planning a compiled version of it (cython)
- Test unit (with python testunit) for the GUI and new widgets
#### Changed
- **ncurses libraries definitively dropped !**  
  Program now requires python 3 only, each single GUI widget, command or
  function is self contained and written in pure python.
  No more extra yaml, ncurses libs or other external deps.
- Version bump (x3). Code refactoring, _ncurses lib entirely dropped_, no
  extra dependencies. Code optimization, no extra features.
- Auto adapting windows on containers/images creation
#### To Do
- pypi version it's still on testing phase and hatchling need few tweaks,
  please use github repo version at the moment. Still a WiP because I'm
  simply focusing on releasing just a single executable, this will be the
  final step before v1.0
- future releases in the 0.x branch will be considered as bugfixes, first
  stable will be labeled as 1.x
---


## [0.2.6] - 2023-12-14 [*Azathoth*]
#### Added
- Standalone, self contained single file application is now ready. If you
  don't want to clone or copy the whole project just take `forklift.app`
  with you on your favorite local or remote host.  
  Self-contained standalone still requires: python, python-ncurses.  
  This is a fully working minified python application ready to run.
#### Changed
- Finally removed yaml library dependency from this project. The only
  dependency is now the ncurses library, there's no need for a virtualenv.
#### To Do
- pypi version it's still on testing phase and hatchling need few tweaks,
  please use github repo version at the moment
---


## [0.2.5] - 2023-12-12 [_Azathoth_]
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


## [0.2.4] - 2023-12-03 [_Azathoth_]
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


## [0.2.3] - 2023-12-01 [_Azathoth_]
First version published on Pypi, still in progress and needs to be fixed there..
#### Changed
- Version alignment from github repo as well as from Pypi packages.
  Release version, no bugfixing
---


## [0.2.0] - 2023-11-07 [_Azathoth_]
#### Added
- Versioning and documentation, license AGPL
- Project initially released on github
- Created as a python package and published on Python official repository.
    "`pip install forklift-container`" to have it installed
- container `logs` command added
#### Changed
- Configuration path as command line parameter
#### To Do
- python unittest on a ncurses widget, how to ?
---


## [0.1.0] - 2023-11-06 [_unknown_]
Officially started as a registered project for
[SUSE Hack Week '23](https://hackweek.opensuse.org/)
#### Added
- Registered to HackWeek '23 as:
[Forklift - Text based GUI utility for dealing with containers](https://hackweek.opensuse.org/23/projects/forklift-text-based-gui-utility-for-dealing-with-containers)
- Built from scratch on top of python+ncurses+yaml, no other deps
#### Changed
- ncurses as a base, widget built from scratch for this project only
#### Fixed
- Fixing ncurses bug on Textbox() class, reported to python standard library
    - cpython official library [issue](https://github.com/python/cpython/issues/111795)
    - cpython library [patch provided](https://github.com/python/cpython/pull/111796)
