# ClusterOps

**ClusterOps** is a Kubernetes operator designed to streamline the initial configuration and 
ongoing maintenance of kubernetes clusters. The focus of this project is primarily on personal
or local installations. However, the goal is to expand its use to encompass all installations
of Kubernetes for local development purposes.  
It simplifies cluster management by automating tasks and providing a user-friendly YAML-based
configuration.


## Features
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


## Getting Started

### Prerequisites
  * A running kubernetes cluster, k3s is tested and supported at the moment.
  * `kubectl` installed and configured to interact with your cluster.

### Installation
1.  **Deploy the ClusterOps Operator:**
<!-- end operations list -->
```yaml
# Work in progress here...
#kubectl apply -f https://raw.githubusercontent.com/andreabenini/podmaster/clusterops/main/deploy/operator.yaml
```
2.  **Create a `ClusterConfig` CRD:**
Define your desired cluster configuration in a YAML file (e.g., `config.yaml`). See the example below for available options.
```yaml
# TO BE DEFINED
```
<!--
apiVersion: clusterops.io/v1alpha1
kind: ClusterConfig
metadata:
  name: my-cluster
spec:
  network:
    plugin: calico
  storage:
    provider: longhorn
  addons:
    - metrics-server
    - ingress-nginx
-->
3.  **Apply the `ClusterConfig`:**
<!-- end list -->
```yaml
kubectl apply -f config.yaml
```

ClusterOps will automatically configure your cluster based on the provided configuration.

## ClusterConfig Options
The `ClusterConfig` CRD allows you to define various aspects of your cluster configuration.
<!--
Here are some of the key options:
  * **network:** Configure the network plugin (e.g., `calico`, `flannel`).
  * **storage:**  Specify the storage provider (e.g., `longhorn`, `openebs`).
  * **addons:**  A list of addons to install (e.g., `metrics-server`, `ingress-nginx`).
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

