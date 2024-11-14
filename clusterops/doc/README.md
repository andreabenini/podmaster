# Kubernetes installation

## Arch Linux (k3s)
```sh
# From AUR, installation as usual
git clone https://aur.archlinux.org/k3s-bin
cd k3s-bin
makepkg -si

# Cluster Installation
./clusterctl --os=arch --kubernetes=k3s install
```
