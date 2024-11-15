# Kubernetes installation

## Arch Linux (k3s)
```sh
# From AUR, installation as usual
git clone https://aur.archlinux.org/k3s-bin
cd k3s-bin
makepkg -si

# Cluster Installation
#./clusterctl --os=arch --kubernetes=k3s install
./clusterctl --os=arch install
```


# Kubernetes removal
## Arch Linux (k3s)
```sh
#./clusterctl --os=arch --kubernetes=k3s remove
./clusterctl --os=arch remove
```
