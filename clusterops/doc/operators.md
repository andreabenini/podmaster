# Operators & Kubernetes

## Installation
`./clusterctl (--os=XYZ) install` already provides `kubebuilder` in the project directory
as a binary, you don't need to install it manually

## Setup a new project
Few simple steps to get started
```sh
mkdir src; cd src

# Create/Init a project
# --repo option must be provided or it won't work
# '--domain example.com' is optional
../kubebuilder init --repo github.com/andreabenini/podmaster/clusterops/src

# Create an API and a controller (CRD: Custom Resource Definition)
# --group   app
# --version v1alpha1     [--group].[--version] API group, so: 'app.v1alpha1'
# --kind ClusterConfig   CRD definition (see config.yml)
../kubebuilder create api --group app --version v1alpha1 --kind ClusterConfig
```
