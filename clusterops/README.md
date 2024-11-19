![ClusterOps logo](icon.png)

# ClusterOps

**ClusterOps** is a Kubernetes installer and operator designed to streamline the initial configuration
and ongoing maintenance of kubernetes clusters. The focus of this project is primarily on personal
or local installations. However, the goal is to expand its use to encompass all installations of
Kubernetes for local development purposes.  
It simplifies cluster management by automating tasks and providing just a user-friendly YAML-based
configuration.


## Overview
  * **Simplified Configuration:** Define your desired cluster state in a simple YAML file, 
    and ClusterOps will handle the rest.
  * **Automated Setup:**  Automates initial k3s cluster configuration, including network settings,
    storage provisioning, special requirements (for example GPUs) and essential component installation.
  * **Ongoing Maintenance:**  Performs routine maintenance tasks such as upgrades, security 
    updates, and resource monitoring.
  * **Extensibility:** Easily extend functionality with custom plugins and configurations.
  * **Self-Healing:** Detects and recovers from common cluster issues, ensuring stability, idempotence
    and reliability. An operation can be performed multiple times without changing the result.
  * **Discreet:** It works only on what it knows, if you are manually configuring parts of your
    cluster and this configuration does not interfere with it you can happily continue to work
    on several parts and use this tool only for what is needed.


## Features
- **distribution and engine independent**. Install your favorite kubernetes engine with your package
manager, execute **_one_** script and you'll have a complete working environment in the system at
your disposal.  
- **Zero config** approach. One single _config.yaml_ file with installation requirements
(add/remove features): human readable, plain and simple. All fancy configs managed automatically
(ingress, balancers, services, proxy, ...).
- **Builtin ContainerHub**.  The default installation provides a fully configured ContainerHub
installed locally along with the kubernetes installation. This configuration allows the user to
build, upload and deploy custom container images as they were provided from an external source.
Internet public sources are still available but local development can be kept in this localhost
server. ClusterOps operator will be fetched from this ContainerHub registry.
- **Kubernetes official dashboard** installed as a plugin, others planned too (k9s for example).
- **Kubevirt** plugin installed and properly configured.  Unleash the power of classic virtualization
(KVM+QEMU) on top of Kubernetes and manage your entire system from there, _libvirtd_ and _virsh_
libs are required.
- _**One operator** to rule them all_. The installation script configures your machine automatically
during installation and adds one kubernetes operator to manage your local cluster. From there the
operator takes care of the cluster on your behalf.
- Clean installation and removal. Just test it, once done uninstall everything without leaving configs
(or pods) behind
<!--TODOs
- Source2Image utility
- Add other distributions: debian, suse, rocky/rhel, gentoo
- Other engines: minicube, KIND, vanilla k8s, CRC
- Monitoring features, alerting and telegram notifications
- NVidia CUDA support for GPUs
- Remote storage, network volumes, object storage
-->


## Getting Started: Installation/Removal
- Prerequisite: `kubectl` CLI utility installed to interact with your cluster.
- See [README](doc/README.md) for details on installation or removal, basically this is valid for
each kubernetes engine and consists of two parts:
  - Install your favorite kubernetes engine with the system defined package manager.
  - Edit your `config.yaml` file to suit your needs (addons plugins, cluster info, virtuazionation).
  - Oneliner instruction to configure it all, from this command an operator will be installed in the
  cluster and will automatically manage everything for you. More or less something like: 
  `./clusterctl --os=YourDistroName install`  
  See [README](doc/README.md) for installation/uninstallation details.


## ClusterConfig Options
The `ClusterConfig` CRD allows you to define various aspects of your cluster configuration.
<!-- some options:
  * **network:** Configure the network plugin (e.g., `calico`, `flannel`).
  * **storage:**  Specify the storage provider (e.g., `longhorn`, `openebs`).
  * **addons:**  A list of addons to install (e.g., `dashboard`, `metrics-server`, `ingress-nginx`).
  * **security:**  Define security settings (e.g., enable pod security policies).
  * **monitoring:**  Configure monitoring tools (e.g., Prometheus, Grafana).
-->


## Contributing
Contributions are welcome\!  
Create a [new issue](https://github.com/andreabenini/podmaster/issues/new/choose),
fork the project or ping the author for further requests.


## License
This project is licensed under the _Affero GPLv3 License_, see the
[LICENSE](./LICENSE) file for details.
