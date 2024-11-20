# Kubevirt: Virtualization made easy
## Requirements
- `libvirt` library and its associated dependencies. Use your package manager for its
installation. It usually creates a systemd service (_libvirtd_) for bare metal VMs.
- `qemu-base`, `qemu-common`, `qemu-tools` (suggested). Usually the installation through the
`qemu` alias (provided on all major linux distributions) is enough. These here listed usually
gather also **vde**, **audio**, **block devices** qemu related packages too. **`virt-manager`**
his handy if you want a UI but it's not strictly needed from the service's perspective.

## Preflight checklist
- `virt-host-validate`. Useful. Major virt/virsh utility to detect your system configuration.
If you want to add new QEMU/LXC capabilities you must start from here to detect what's available
and what is not. Fix misconfigurations and restart.
- https://kubevirt.io/user-guide/cluster_admin/installation/ Official documentation guide, this
is THE reference for everything about it. Pay special attention to secure libs like:
`apparmor`, `selinux`.


## Installation
Kubevirt installation basically relies on their default operator, no changes here, it just works
out of the box.
```sh
# Point at latest release
RELEASE=$(curl https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)

# Deploy the KubeVirt operator
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/${RELEASE}/kubevirt-operator.yaml

# Create the KubeVirt CR (instance deployment request) which triggers the actual installation
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/${RELEASE}/kubevirt-cr.yaml

# wait until all KubeVirt components are up
kubectl -n kubevirt wait kv kubevirt --for condition=Available
```
Next step is the virtctl CLI utility, highly recommended for:
- Serial and graphical console access
- Starting and stopping VirtualMachineInstances (VMI, as CRD)
- Uploading virtual machine disk images
- Live migrating VirtualMachineInstances (VMI) and/or canceling live migrations. This feature is
not ready yet on a mononode k3s cluster.

```sh
# virtctl installation (in [clusterops] directory)
RELEASE=$(curl https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)
wget https://github.com/kubevirt/kubevirt/releases/download/${RELEASE}/virtctl-${RELEASE}-linux-amd64
# Easy soft link for it
ln -s virtctl-$RELEASE-linux-amd64 virtctl
chmod +x virtctl
```

## Tests
```sh
# Get a VM sample, all machines are defined through a yaml file, as usual for pods
# Virtual Machine is an OpenStack sample vm named cirros
kubectl apply -f https://kubevirt.io/labs/manifests/vm.yaml
#> virtualmachine.kubevirt.io/testvm created

# Start newly created virtual machine, name:[testvm]
./virtctl start testvm
#> VM testvm was scheduled to start

# Get virtual machines information
kubectl get vmi
#> NAMESPACE     NAME     AGE   PHASE     IP           NODENAME   READY
#> kube-system   testvm   55s   Running   10.42.0.17   n1         True
kubectl get vm 
#> NAME     AGE     STATUS    READY
#> testvm   6m46s   Running   True

kubectl get pods -A | grep virt-launcher
#> kube-system  virt-launcher-testvm-jggr2  3/3  Running  0  8m38s

# Exposing virtual machines on port SSH (using k8s NodePort)
./virtctl expose vmi testvm - name=testvm-ssh - port=22 - type=NodePort
#> Service testvm-ssh successfully exposed for vmi testvm
# ...same on http 8080
./virtctl expose vmi testvm - name=testvm-http - port=8080 - type=NodePort
#> Service testvm-http successfully exposed for vmi testvm

# Open a console, like OpenStack
# I'm using OldGlory cirros image from OpenStack, so user/passwords: cirros/gocubsgo
./virtctl console testvm
```
