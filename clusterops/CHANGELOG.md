# clusterops Change Log
All notable changes to this project will be documented in this file.


## [0.1.1] - 2024-11-26 [_Attila_]
#### Added
- openSUSE / SUSE Linux Enterprise Server / Tumbleweed installation
- Documentation notes on SUSE Linux operating systems
#### Changed
- linux arch python installation. More clear and verbose process to better cover
all use cases
- linux arch disinstallation. Improved cleanup of stale resources, volumes, unused
containers (leftovers) after the complete removal process
#### To Do
- Finite state machine process across the kubernetes go operator to completely
    cover installation and cluster self healing
- Test unit and coverage for the go operator
- Add other major linux distributions
- Add other kubernetes engine
---


## [0.1.0] - 2024-11-18 [_unknown_]
Officially started as a registered project for
[SUSE Hack Week '24](https://hackweek.opensuse.org/)
#### Added
- Registered to HackWeek '24 as:
[ClusterOps - Easily install and manage your personal kubernetes cluster](https://hackweek.opensuse.org/24/projects/clusterops)
- Built from scratch with python and go
- k3s is the first working kubernetes engines, others will follow later
- arch linux is the first targeted Linux Distribution due to internal resources available
#### Changed
- CLI Installer and K8s Operator are the barebone of the project
#### Fixed
- Fixing installation and basic setup to cover the entire configuration, other distros will follow shortly
