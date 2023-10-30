# Simple Perl 5 program with CPAN on Red Hat UBI minimal
#
# @see  Tested on: podman, docker
# @see  - copy perl.env.rc in your working directory to use it
#       - Perl program: '{{ input("filename", "Perl filename", None) }}'
#       - Username: '{{ input("username", "Container user name", "root") }}'
FROM registry.access.redhat.com/ubi8/ubi-minimal:latest

# Software installation
# perl5, cpan (and cpan build tools: make, gcc)
RUN microdnf install -y perl
RUN microdnf install -y cpanminus
RUN microdnf install -y make
RUN microdnf install -y gcc

# CPAN software installation
RUN cpanm JSON
RUN cpanm boolean
# RUN ...

# Install additional software and utilities
RUN microdnf install -y vim
RUN microdnf install -y git

# CPAN library automatic configuration fix
RUN (echo y;echo o conf prerequisites_policy follow;echo o conf commit)|cpan

# Entering the perl environment so I don't have to do it manually each single time
# Please adjust .bashrc location to your suitable user directory (if any)
RUN mkdir /{{basename("filename")}}; \
    chown {{var("username")}}:{{var("username")}} /{{basename("filename")}}; \
    echo -e "\n\nalias ls='ls --color=auto'" >> /{{var("username")}}/.bashrc; \
    echo -e "\n# Set perl environment\nsource perl.env.rc" >> /{{var("username")}}/.bashrc

# Environment setup
WORKDIR /{{basename("filename")}}
ADD {{var("filename")}} /{{basename("filename")}}

# Set an entry point
CMD ["bash"]
# or change it to your perl program
# CMD ["perl", "/{{basename("filename")}}/{{var("filename")}}]
