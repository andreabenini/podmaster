![Forklift logo](icon.png)

# Forklift - Text based utility for dealing with containers
### What is this for
This is a simple and handy text based GUI utility for dealing with boring
and repetitive tasks while managing containers.  
If you usually manage them in your daily activities you'll surely deal
a lot with the CLI and execute repetitive commands for: 
building images, creating containers, running, killing and stopping
them all the time.  

It doesn't really matter if you are a Developer, a DevOps or a SRE;
most of your time might be spent on the CLI for deleting/respawning/starting
new instances for your favorite product.  
You can surely do it from a GUI or editor (vscode, eclipse, ...)
but it might be messy if you're managing them remotely through SSH and 
all you have at your disposal is just your trusty text-only shell connection.  

That's the reason for this simple, quick, text-only curses based utility,
no matter if containers are running on a remote machine, locally or if you
prefer a specific Window Manager.
I expressly don't want to rely on X11/Wayland, infinite dependencies 
(or keep them to the bare minimum) and it has to be text-only and usable from
a remote shell.  
This utility relies on: python (+yaml) and curses bindings (just plain curses,
no extra widgets required).  
It is not a fully fledged solution but rather a small and quick tool for
running boring tasks, you'll still use docker/podman of your choice but you
don't want to be annoyed by usual and repetitive commands
    (`docker ps -a; docker kill <ID>; docker start <ID> <params, ...>`).
That's what this utility is about.

#### Rolling demo overview
[![Screenshot overview](contrib/rollingdemo.mp4)](contrib/rollingdemo.mp4)

---
