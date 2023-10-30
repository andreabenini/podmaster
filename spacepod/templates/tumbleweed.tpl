# SUSE Tumbleweed minimal image (Work in Progress)
# TODO: This was a test, recreate a new minimal image on top of it
#
# @see  Tested on: podman, docker
#
# registry.opensuse.org/opensuse/tumbleweed:latest
# registry.opensuse.org/opensuse/tumbleweed-dnf:latest
# registry.opensuse.org/opensuse/tumbleweed-microdnf:latest
FROM registry.opensuse.org/opensuse/tumbleweed-microdnf:latest
#       - Username: '{\{ input("username", "Container user name", "root") }}'

# Software installation
# RUN microdnf install -y gcc

# RUN ...
# Install additional software and utilities
# XXX: Adding packages
#RUN microdnf install -y vim
#RUN microdnf install -y git

# Entering the perl environment so I don't have to do it manually each single time
# Please adjust .bashrc location to your suitable user directory (if any)
# XXX: Running arbitrary commands once done
# RUN mkdir /{{basename("filename")}}; \
#     chown {{var("username")}}:{{var("username")}} /{{basename("filename")}}; \
#     echo -e "\n\nalias ls='ls --color=auto'" >> /{{var("username")}}/.bashrc; \
#     echo -e "\n# Set perl environment\nsource perl.env.rc" >> /{{var("username")}}/.bashrc

# Environment setup
# WORKDIR /{{basename("filename")}}
# ADD {{var("filename")}} /{{basename("filename")}}

# Set an entry point
CMD ["bash"]
# or change it to your program
# CMD ["perl", "/{{basename("filename")}}/{{var("filename")}}]


# podman build -t tumbleweed .
# podman run -it tumbleweed /bin/bash