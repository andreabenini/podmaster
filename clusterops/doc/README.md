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


## openSUSE / SLES / Tumbleweed (k3s)
### K3s installation
```sh
# Easily install it from k3s.io
curl -sfL https://get.k3s.io | sh -
```
>    From docs in https://k3s.io/ and
>    https://software.opensuse.org/package/k3s it seems there's no official _rpm_
>    installation package and installation is almost left to these methods:
>    ```sh
>    # Official method from k3s.io (highly suggested)
>    curl -sfL https://get.k3s.io | sh -
>
>    # OpenSUSE suggestions from community packages:
>    https://software.opensuse.org/package/k3s
>
>    # Getting ready made binary releases from github
>    https://github.com/k3s-io/k3s/releases
>    #...and follow official install method
>    curl -sfL https://get.k3s.io | sh -
>    ```
>    First method here reported is the suggested (and easy) one.  
>    Packages like `k3s-install` conflicts with `kubernetes-client-provider` that
>    contains binary:`kubectl` so it's probably better to avoid them.
### clusterctl install
```sh
# ./clusterctl --os=suse --kubernetes=k3s install
./clusterctl --os=suse install
```



# Kubernetes removal
## Arch Linux (k3s)
```sh
#./clusterctl --os=arch --kubernetes=k3s remove
./clusterctl --os=arch remove
```

## openSUSE / SLES / Tumbleweed (k3s)
```sh
#./clusterctl --os=arch --kubernetes=k3s remove
./clusterctl --os=suse remove
```
