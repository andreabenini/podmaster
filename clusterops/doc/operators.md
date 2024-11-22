# Operators & Kubernetes

## Installation
`./clusterctl (--os=XYZ) install` already provides `kubebuilder` in the project directory
as a binary, you don't need to install it manually

## Setup a new project
- Few simple steps to get started
    ```sh
    # Create a project sources directory
    mkdir src; cd src

    # Create/Init a project
    # --repo option must be provided or it will not work
    # '--domain example.com' is optional
    ../kubebuilder init --repo github.com/andreabenini/podmaster/clusterops/src

    # Create an API and a controller (CRD: Custom Resource Definition)
    # --group   app
    # --version v1alpha1     [--group].[--version] API group, so: 'app.v1alpha1'
    # --kind ClusterConfig   CRD definition (see config.yml)
    ../kubebuilder create api --group app --version v1alpha1 --kind ClusterConfig
    cd ..
    ```
- Rename samples dir to _[clusterops]_ or whatever name you prefer
- Add your custom files in the newly renamed directory
- Edit _[clusterops/kustomization.yaml]_ to reflect your changes
- Open `./src/internal/controller/clusterconfig_controller_test.go` and
    `./src/internal/controller/clusterconfig_controller.go` files
- [onetime] Edit `Makefile` and adapt _$CONTAINER_TOOL_ variable, you need to do
    it just once, in my case it's just a matter of selecting _podman_ instead of
    _docker_
    ```Makefile
    CONTAINER_TOOL ?= podman
    ```
- Make manifest files: `make manifests`
- Build the operator image
    ```sh
    # make docker-build IMG=<your-docker-image>:<tag>
    make docker-build IMG=clusterconfig:0.1
    ```
    if an error is raised like:
    ```txt
    > podman build -t clusterconfig:0.1 .
    > [1/2] STEP 1/11: FROM golang:1.22 AS builder
    > Error: creating build container: short-name "golang:1.22" did not resolve to an alias and no unqualified-search registries are defined in "/etc/containers/registries.conf"
    > make: *** [Makefile:106: docker-build] Error 125
    ```
    it's probably related to the deprecated behavior of fetching short names
    from the makefile, newer syntax plans to always use FQDN while fetching
    images. This is a discouraged sytanx the makefile is still using, to
    solve it you can:
    - Change the `Makefile` (_docker-build_) section, I advise against that
    - Revert back to older syntax by changing container registry behavior
      ```txt
      cat <<EOT > 01-containerhub.conf
      unqualified-search-registries = ["localhost:5000", "docker.io"]

      [[registry]]
      location = "localhost:5000"
      insecure = true

      [[registry]]
      location = "docker.io"
      insecure = false

      EOT
      ```
    - Rebuild the image once done (`make docker-build IMG=clusterconfig:0.1`)
      ```txt
      ...
      Successfully tagged localhost/clusterconfig:0.1
      f0e28ef53f4b69d7abbd5444104f482a6e15fe694aca029df05b78f3cac9b462
      ```
    - Check current image availability
      ```sh
      podman images -a |grep clusterconfig
      > localhost/clusterconfig 0.1 f0e28ef53f4b  5 minutes ago  73.2 MB
      ```
- Push image to the ContainerHub repository
    ```sh
    # Syntax 'make docker-push IMG=<your-docker-image>:<tag>'
    # Adding localhost ContainerHub to push it locally
    make docker-push IMG=localhost:5000/clusterconfig:0.1
    ```
- Deploy the image from the ContainerHub
    ```sh
    # Syntax 'make deploy IMG=<your-docker-image>:<tag>'
    # Adding localhost ContainerHub to deploy it locally
    make deploy IMG=localhost:5000/clusterconfig:0.1
    ```
