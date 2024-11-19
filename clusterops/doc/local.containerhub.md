# Localhost ContainerHub HOWTO
To set up a local Container registry (a local "Container Hub") and configure it for use with the local
Kubernetes installation the following procedure will be applied:

### Configuration
- Setup a local container registry.  
  A container registry can be run as a container using the official **`registry`** image.
  This creates a local registry accessible at `http://localhost:5000`.
    ```sh
    # -d detached mode   Work as a daemon and detach from the shell
    # -p <local:exposed> map TCP 5000 to 5000 [default registry port]
    # --restart=always   ensure automatic restart on crash
    # --name registry    give the container a friendly name
    # -v ...             create a PV named [registry-data]
    # docker.io/URL      full URL with the official registry image
    podman run -d -p 5000:5000 --restart=always --name registry \
                  -v registry-data:/var/lib/registry docker.io/library/registry:2
    # oneshot for a systemd service:
    # podman run -p 5000:5000 --restart=always --name registry -v registry-data:$(pwd)/registry docker.io/library/registry:2
    ```
- Verify service status
    ```sh
    curl http://localhost:5000/v2/
    # an empty '{}' response if it's running
    ```

### Image upload
- Push an image to the Local Registry
    ```sh
    # Tag myImage as latest in the repository
    podman tag myImage:latest localhost:5000/myImage:latest
    # Now push it
    podman push localhost:5000/myImage:latest
- Verify the image and check the contents of the registry
    ```sh
    curl http://localhost:5000/v2/_catalog
    ```

### Configure K3s to Use the Local Registry
- K3s uses containerd as its container runtime. To integrate it with the local podman registry, 
    a ContainerHub has to be configured. If the registry doesn’t use HTTPS, configure K3s
    to allow an insecure registry.  
    Create the file `/etc/rancher/k3s/registries.yaml` with this content:
    ```yml
    mirrors:
        "localhost:5000":
            endpoint:
            - "http://localhost:5000"
    # Add interfaces if you'd like to expose on the local LAN too
    #   "192.168.x.x:5000":
    #       endpoint:
    #       - "http://192.168.x.x:5000"
    ```
- Restart K3s service to apply the new configuration
    ```sh
    sudo systemctl restart k3s
    ```

### Use local registry
When specifying an image for the Kubernetes workloads, local registry is now available
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myApp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myApp
  template:
    metadata:
      labels:
        app: myApp
    spec:
      containers:
      - name: myApp
        image: localhost:5000/myImage:latest
```
