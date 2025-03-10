# -*- coding: utf-8 -*-
#
# @description      container management class
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              Containers and images class for dealing with basic operations (list, stop, remove, kill, ...)
#
# pyright: reportMissingImports=false
#
import os
import yaml
import stat
import requests

from .system import System

class Kubernetes():
    def __init__(self, engine='', osType='', homeConfigFile='~/.kube/config'):
        self.__homeconfigfile = homeConfigFile
        self.__containerRegistry = 'registry'
        self.__volumeRegistry = 'clusterops-registry'
        self.__setKubernetesEngine(engineName=engine)           # k3s, minikube, kind, ...
        self.__detectContainerRuntime(['docker', 'podman'])     # Add here supported container runtimes
        self.__dirConfig = System.programPath + os.path.sep + 'config' + os.path.sep
        self.__fileService = self.__dirConfig + "clusterops.service"
        self.__systemdService = '/etc/systemd/system/clusterops.service'
        self.__loadConfig()
        self.__os = osType
    @property                       # Operating system: arch, suse, debian, rhel, gentoo, ...
    def os(self):
        return self.__os
    @property                       # Kubernetes engine type: k3s, minikube, kind, ...
    def engine(self):
        return self._engine
    @property                       # Container engine [__runtime] and its path [__runtimePath]: podman, docker
    def runtime(self):
        return self.__runtime
    @property                       # Container 'registry' name [registry]
    def containerRegistry(self):
        return self.__containerRegistry
    @property                       # Container 'registry' associated volume name [clusterops-registry]
    def volumeRegistry(self):
        return self.__volumeRegistry

    # Save/Load kubernetes working configuration
    def __saveConfig(self):
        try:
            with open(self.__dirConfig+"setup.yaml", "w+") as yamlFile:
                yaml.dump(self.__config, yamlFile, indent=4) 
        except Exception as E:
            pass
    def __loadConfig(self):
        try:
            with open(self.__dirConfig+"setup.yaml", "r") as yamlFile:
                self.__config = yaml.safe_load(yamlFile)
                return
        except Exception as E:
            pass
        self.__config = {'information':'this file has been automatically generated by clusterctl to keep its status, do not delete it'}

    # Change the cluster name, local setup for user in the ~/.kube/config file
    def __changeClusterName(self, configurationFile, clusterName):
        print(f"- Changing local kubernetes name to '{clusterName}'")
        configurationFile = os.path.realpath(os.path.expanduser(configurationFile))
        # Load user's configuration file
        with open(configurationFile, 'r') as file:
            data = yaml.safe_load(file)
        # Apply changes (4 entries)
        data.setdefault("clusters", [{}])
        data['clusters'][0].setdefault('name', '')
        data['clusters'][0]['name'] = clusterName
        data.setdefault("contexts", [{}])
        data['contexts'][0].setdefault('name', '')
        data['contexts'][0]['name'] = clusterName
        data['contexts'][0].setdefault('context', {})
        data['contexts'][0]['context']['cluster'] = clusterName
        data['current-context'] = clusterName
        # Save changes back to the file
        with open(configurationFile, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

    def __setKubernetesEngine(self, engineName):
        self._engine = engineName
        # 'self.engine' might be different from '{self.engine}.service', 
        # that's why there is this ugly if..then statement block here
        if self.engine == 'k3s':        
            self._engineServiceName = self.engine

    # Detect container runner (podman, docker, ...)
    def __detectContainerRuntime(self, platforms):
        self.__runtime = self.__runtimePath = None
        if platforms:
            element = platforms[0]
            tail = platforms[1:]
            (_, _, errorCode) = System.Exec(f"{element} --version")
            if errorCode == 0:
                self.__runtime = element
                (element, _, _) = System.Exec(f"which {element}")
                self.__runtimePath = element.strip()
            else:
                self.__detectContainerRuntime(tail)


    # Installing google kubebuilder sdk utility for operator creation and management
    def install_kubebuilderUtility(self):
        kubebuilder = System.programPath+os.path.sep+'kubebuilder'
        print(f"- Installing kubebilder sdk as '{kubebuilder}'")
        (operatingSystem, _, _) = System.Exec("go env GOOS")
        (architecture, _, _)    = System.Exec("go env GOARCH")
        url = f"https://go.kubebuilder.io/dl/latest/{operatingSystem.strip()}/{architecture.strip()}"
        print(f"    {url}")
        (error, message) = System.downloadFile(url=url, filename=kubebuilder)
        if error==False:
            System.Exit(f"Cannot download 'kubebuilder' from {url}\nERROR: {message}")
        chmodPermissions = os.stat(kubebuilder).st_mode
        os.chmod(kubebuilder, chmodPermissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)   # Adding +x
        print(f"    File saved as: {kubebuilder}")


    # Create a dedicated systemd service named clusterops.service with the ContainerHub
    def install_clusteropsService(self):
        print(f"- Installing dedicated {os.path.basename(self.__systemdService)}")
        try:
            with open(self.__fileService, 'r') as file:
                serviceContent = file.read()
                serviceContent = serviceContent.replace('{serviceRequired}', self._engineServiceName)
                serviceContent = serviceContent.replace('{user}', str(os.getuid()))
                serviceContent = serviceContent.replace('{path}', System.programPath)
                serviceContent = serviceContent.replace('{runtime}', self.__runtimePath)
                serviceContent = serviceContent.replace('{containerName}',  self.containerRegistry)
                serviceContent = serviceContent.replace('{volumeRegistry}', self.volumeRegistry)
                print(f"    - Create/Edit '{self.__systemdService}'")
                System.Exec(f'sudo tee {self.__systemdService}', stdInput=serviceContent)
                print(f"    - systemctl daemon-reload")
                System.Exec(f'sudo systemctl daemon-reload')
                print(f"    - Starting '{self.__systemdService}'")
                System.Exec(f'sudo systemctl start clusterops')
        except FileNotFoundError:
            System.Exit(f"File '{self.__fileService}' not found, cannot install {os.path.basename(self.__systemdService)}")
        except Exception as E:
            System.Exit(f"Error while creating {os.path.basename(self.__systemdService)}: {str(E)}")

    # Installing plugin kubernetes dashboard
    def install_KubernetesDashboard(self, config):
        print('- Installing Kubernetes Dashboard')
        if 'url' not in config:
            System.Exit("Dashboard configuration url not found, please add it to the config.yml file\nERROR: parameter: {'url': 'https://kubernetes.dashboard/url'}, see examples")
        if not os.path.exists(self.__dirConfig+'dashboard.yaml'):
            System.Exit(f"Dashboard configuration file '{self.__dirConfig+'dashboard.yaml'}' does not exists")
        System.Exec(f'kubectl apply -f {config["url"]}', printOutput=True)
        System.Exec(f'kubectl apply -f {self.__dirConfig+"dashboard.yaml"}', printOutput=True)
        print()


    # Installing plugin KubeVirt
    def install_KubernetesKubeVirt(self):
        print("- Installing KubeVirt")
        print("    - Fetching latest release version number")
        self.install_KubernetesKubeVirt_getVersion()
        version = self.__config['kubevirt']['version']
        print("    - Deploy the KubeVirt operator")
        System.Exec(f'kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/{version}/kubevirt-operator.yaml', printOutput=True)
        print("    - Create the KubeVirt CR to trigger the installation")
        System.Exec(f'kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/{version}/kubevirt-cr.yaml', printOutput=True)
        print("    - Waiting the operator setup")
        System.Exec(f'kubectl -n kubevirt wait kv kubevirt --for condition=Available')
        print("    - Downloading 'virtctl' utility")
        file_virtctl = System.programPath+os.path.sep+'virtctl'
        url_virtctl  = f'https://github.com/kubevirt/kubevirt/releases/download/{version}/virtctl-{version}-linux-amd64'
        print(f"      {url_virtctl} -> {os.path.basename(file_virtctl)}")
        System.fileDelete(file_virtctl)
        (error, message) = System.downloadFile(url=url_virtctl, filename=file_virtctl)
        if error==False:
            System.Exit(f"Cannot download 'virtctl' from {url_virtctl}\nERROR: {message}")
        chmodPermissions = os.stat(file_virtctl).st_mode
        os.chmod(file_virtctl, chmodPermissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)   # Adding +x
        print(f"      File saved as: {file_virtctl}")


    # Fetches the latest stable KubeVirt release version from the official sources
    def install_KubernetesKubeVirt_getVersion(self):
        url = "https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt"
        try:
            response = requests.get(url)
            response.raise_for_status()                                             # Raise Exception for bad status codes
            self.__config.setdefault("kubevirt", {})
            self.__config["kubevirt"].setdefault("version", response.text.strip())  # Getting current kubevirt version
            self.__saveConfig()
        except requests.exceptions.RequestException as e:
            System.Exit(f"Error fetching KubeVirt release version: {e}")


    # Install the kubernetes operator clusterops
    def install_KubernetesOperator(self):
        print(f"\n- Installing kubernetes operator")
        # ContainerHub configuration
        fileSource=self.__dirConfig+'01-containerhub.conf'
        fileDestination='/etc/containers/registries.conf.d/01-containerhub.conf'
        print(f"    - ContainerHub configuration")
        print(f"      cp {os.path.basename(fileSource)} -> {os.path.dirname(fileDestination)}")
        System.Exec(f"sudo cp '{fileSource}' '{fileDestination}'")
        # Rebuild, Publish & Deploy operator
        print(f"    - Kubernetes operator (rebuild,publish,deploy)")
        System.Exec(f"{System.programPath + os.path.sep}deploy.operator.sh", printOutput=True)
        print(f"")


    # Install and configure K3S on Arch Linux
    def install_arch_k3s(self, config):
        self.__install_generic_k3s(config=config)

    # Install and configure K3S on SUSE Linux related OSes
    def install_suse_k3s(self, config):
        # Fixing crappy apparmor location, mostly on tumbleweed/openSUSE
        # When apparmor_parser is installed is getting wrong information when it's executed
        #   from a regular user, having it in the same apparmor dir seems to solve this issue
        System.Exec("sudo ln -s /usr/local/bin/k3s /usr/sbin/k3s")      # /usr/sbin is where apparmor is
        # now standard install
        self.__install_generic_k3s(config=config)

    def __install_generic_k3s(self, config):
        # Starting k3s for the first time to generate k3s.yaml
        (_,_,status) = System.Exec('systemctl is-active k3s')
        if status!=0:
            print("- Starting k3s service")
            System.Exec("sudo systemctl start k3s")
            (_,_,status) = System.Exec("systemctl is-active k3s")
            if status!=0:
                System.Exit("Cannot start k3s, aborting installation")
        else:
            print("- k3s service is already active")
        # Kubernets configuration setup
        self.__install_kubernetesConfiguration('/etc/rancher/k3s/k3s.yaml', config)
        # sysctl configuration setup
        System.Exec("sudo sh -c 'echo -e \"# Enable IPv4 forwarding for internal kubernetes pods\nnet.ipv4.ip_forward=1\" > /etc/sysctl.d/k3s.conf'")
        System.Exec("sudo sysctl --load /etc/sysctl.d/k3s.conf")
        print(f"- Configuration completed\n")
        # Display kubernetes cluster information
        print(f"[Cluster Information]")
        System.Exec('sudo k3s kubectl cluster-info', printOutput=True)
        (stdout,_,status) = System.Exec('sleep 2 && kubectl get nodes 2>&1')    # Check if this output is displayed
        print(f"[Nodes] ({status})\n{stdout}\n")
        print("[k3s check-config]")
        System.Keypress()
        System.Exec('sudo k3s check-config', printOutput=True)
        print("     apparmor error here reported is expected when apparmor is not installed or configured")
        print("")


    # Create kubernetes configuration for the user by taking it from the cluster installation
    def __install_kubernetesConfiguration(self, kubernetesConfigurationFile, config):
        print("- Kubernetes user configuration file setup")
        homeConfigurationFile = os.path.expanduser(self.__homeconfigfile)
        System.Exec(f'mkdir -p {os.path.dirname(homeConfigurationFile)}')
        if os.path.exists(homeConfigurationFile):
            (_,_,status) = System.Exec(f'sudo diff {kubernetesConfigurationFile} {homeConfigurationFile}')
            if status != 0:
                print(f"\nYour local configuration differs from kubernetes system config")
                print(f"    -> {kubernetesConfigurationFile}")
                print(f"    -> {homeConfigurationFile}")
                if System.Confirm(Message='    Do you want to overwrite yours with kubernetes default [y|N] ? ', Confirm=['y','yes']):
                    self.__install_kubernetesConfiguration_userFile(fileSrc=kubernetesConfigurationFile, fileDest=homeConfigurationFile, config=config)
                else:
                    print("\n- Keeping kubernetes user configuation file, no changes")
        else:
            self.__install_kubernetesConfiguration_userFile(fileSrc=kubernetesConfigurationFile, fileDest=homeConfigurationFile, config=config)

    # Copy kubernetes configuration to local user
    def __install_kubernetesConfiguration_userFile(self, fileSrc=None, fileDest=None, config=None):
        print("\n- Creating the user configuration file from the kubernetes service")
        System.Exec(f'sudo cp {fileSrc} {fileDest}; sudo chown {os.getuid()}:{os.getgid()} {fileDest}')
        self.__changeClusterName(fileDest, config['metadata']['name'])


    # Remove ContainerHub from the system
    def remove_clusteropsService(self):
        print(f"- Removing dedicated {os.path.basename(self.__systemdService)}")
        try:
            # Removing clusterops.service
            print(f"    - Stopping {os.path.basename(self.__systemdService)}")
            System.Exec(f'sudo systemctl stop {os.path.basename(self.__systemdService)}')
            print(f"    - Removing {os.path.basename(self.__systemdService)}")
            System.Exec(f'sudo rm {self.__systemdService}')
            print(f"    - systemctl daemon-reload")
            System.Exec(f'sudo systemctl daemon-reload')
            # Remove registry container and image
            print("    - Removing registry container")          # Getting imagename from the container named 'registry'
            (containerImageName, _, _) = System.Exec(self.runtime+' ps -a --format "{{.Image}} <<{{.Names}}>>" | grep  "<<registry>>" | sed "s/ .*//"')
            if containerImageName.strip() != '':
                System.Exec(f'{self.runtime} stop {self.containerRegistry}')
                System.Exec(f'{self.runtime} rm  --force {self.containerRegistry}')
                System.Exec(f'{self.runtime} rmi --force {containerImageName.strip()}')
            # Remove registry volume
            print("    - Removing registry volume")
            System.Exec(f"{self.runtime} volume rm --force {self.volumeRegistry}")
        except FileNotFoundError as E:
            System.Exit(f"Failing removal of {os.path.basename(self.__systemdService)}. File not found: {str(E)}")
        except Exception as E:
            System.Exit("Error while removing {os.path.basename(self.__systemdService)}: "+str(E))


    # Remove kubernetes dashboard
    def remove_KubernetesDashboard(self, config):
        print('- Removing Kubernetes Dashboard')
        if 'url' not in config:
            System.Exit("Dashboard configuration url not found, please add it to the config.yml file\nERROR: parameter: {'url': 'https://kubernetes.dashboard/url'}, see examples")
        if not os.path.exists(self.__dirConfig+'dashboard.yaml'):
            System.Exit(f"Dashboard configuration file '{self.__dirConfig+'dashboard.yaml'}' does not exists")
        System.Exec(f'kubectl delete -f {self.__dirConfig+"dashboard.yaml"}', printOutput=True)
        System.Exec(f'kubectl delete -f {config["url"]}', printOutput=True)
        print()


    # Removing Kubevirt installation
    def remove_KubernetesKubeVirt(self):
        self.__config.setdefault("kubevirt", {})
        if 'version' not in self.__config['kubevirt']:
            self.install_KubernetesKubeVirt_getVersion()
        version = self.__config['kubevirt']['version']
        print(f"- Removing KubeVirt {version}")
        print("    - Removing the KubeVirt CR triggered in the installation")
        System.Exec(f'kubectl delete -f https://github.com/kubevirt/kubevirt/releases/download/{version}/kubevirt-cr.yaml', printOutput=True)
        print("    - Removing the KubeVirt operator")
        System.Exec(f'kubectl delete -f https://github.com/kubevirt/kubevirt/releases/download/{version}/kubevirt-operator.yaml', printOutput=True)
        print(f"    - Removing 'virtctl' utility")
        System.fileDelete(System.programPath+os.path.sep+'virtctl')
        print(f"    - Removing stale dirs: /run/kubevirt /var/lib/kubevirt")
        System.Exec('sudo rm -rf /var/lib/kubevirt /var/lib/kubevirt-node-labeller /run/kubevirt /run/kubevirt-private /run/kubevirt-libvirt-runtimes')
        del self.__config['kubevirt']
        self.__saveConfig()


    # Drain the kubernetes cluster
    def remove_drainKubernetes(self):
        (_,stderr,status) = System.Exec('systemctl is-active k3s')
        if status!=0:
            System.Exit(f"Cannot remove containers, k3s service is not available\n{stderr}")
        # Deleting traefik and metrics
        print("- Wiping traefik pods and system daemon")
        System.Exec("kubectl delete all -l app.kubernetes.io/name=traefik -n kube-system 2>/dev/null", printOutput=True)
        print("- Metrics server have some storage space, wiping it directly")
        System.Exec("kubectl delete all -l k8s-app=metrics-server -n kube-system")
        # Draining the node
        (nodeName, stderr, status) = System.Exec("kubectl get nodes -o name|sed 's#node/##'")
        print(f"- Draining the node '{nodeName.strip()}'")
        if status != 0:
            System.Exit(f"Cannot detect cluster [nodeName]:  kybectl get nodes -o name\n{stderr}")
        System.Exec(f"kubectl drain {nodeName.strip()} --ignore-daemonsets --delete-emptydir-data", printOutput=True)
        print("- Stopping k3s service")
        System.Exec(f'sudo systemctl stop k3s')
        # Dropping hanged volumes
        print("- Umounting stale volumes")
        System.Exec("sudo df |grep /var/lib/kubelet |awk '{ print $6}' |xargs -I % sudo umount %")
        System.Exec("sudo df |grep /run/k3s         |awk '{ print $6}' |xargs -I % sudo umount %")
        pathContainers = "/var/lib/rancher/k3s /run/k3s /var/lib/kubelet /run/containerd/runc/k8s.io"
        print(f"- Removing containers work directories: [{pathContainers}]")
        System.Exec(f'sudo rm -rf {pathContainers}', printOutput=True)
        # Removing google kubebuilder utility
        print("    - Removing kubebuilder")
        System.fileDelete(System.programPath+os.path.sep+'kubebuilder')


    # [ARCH] Removing possible configurations from filesystem
    def remove_arch_k3s_configuration(self, config):
        self.__remove_generic_k3s_configuration(config=config)

    # [SUSE] Removing possible configurations from filesystem
    def remove_suse_k3s_configuration(self, config):
        self.__remove_generic_k3s_configuration(config=config)

    # Default configuration removal
    def __remove_generic_k3s_configuration(self, config):
        pathETC        = "/etc/rancher/k3s"
        pathSYSCTL     = "/etc/sysctl.d/k3s.conf"
        pathKUBECONFIG = os.getenv("HOME")+os.path.sep+'.kube'
        System.Exec(f'sudo rm -rf {pathKUBECONFIG} {pathETC} {pathSYSCTL}')


    # [ARCH] Removing binaries and uninstalling packages
    def remove_arch_k3s_binaries(self, config):
        System.Exec("sudo pacman -Rsn --noconfirm k3s-bin", printOutput=True)

    # [SUSE] Removing binaries, no binaries provided for suse
    def remove_suse_k3s_binaries(self, config):
        self.__remove_generic_k3s_binaries(config=config)

    # Official method of removing binaries with classic installation: "curl -sfL https://get.k3s.io | sh -"
    def __remove_generic_k3s_binaries(self, config):
        # No installation package, manual uninstall of all leftovers
        System.Exec(f'sudo /usr/local/bin/k3s-killall.sh')
        System.Exec(f'sudo /usr/local/bin/k3s-uninstall.sh')
        # Removing custom locations
        System.Exec("sudo rm -rf /usr/sbin/k3s")        # See install_suse_k3s() for details
