#!/usr/bin/env sh
#
#
#
VERSION=0.1

# Function to build the image
build() {
    echo "- Building the image..."
    cd src
    echo "    - Manifest creation" && \
    make manifests && \
    echo "    - Image build" && \
    make docker-build IMG=clusterconfig:$VERSION
    cd $SCRIPTS_DIR
}

# Function to push the image to a registry
push() {
    echo "- Pushing the image"
    cd src
    make docker-push IMG=localhost:5000/clusterconfig:$VERSION
    cd $SCRIPTS_DIR
}

# Function to deploy the image
deploy() {
    echo "- Deploying the image"
    cd src
    make deploy IMG=localhost:5000/clusterconfig:$VERSION
    cd $SCRIPTS_DIR
}


printHelp() {
    echo -e "usage: $(basename $0) (build|push|deploy)\n"
    echo -e "Rebuild, Publish, Deploy the clusterops operator\n\npositional arguments:"
    echo -e "    (build|push|deploy) The command to execute"
    echo -e "                        when argument is not supplied it executes them all\n"
    echo -e "options:"
    echo -e "    -h, --help          show this help message and exit\n\n"
}

#
# MAIN
#
WORK_DIR=$(pwd)
SCRIPTS_DIR=$(dirname $0)
cd "$SCRIPTS_DIR"
# Check input parameters, if any
if [ $# -eq 0 ]; then       # No parameters, execute all functions
    build
    echo
    push
    echo
    deploy
else
    # Parameter supplied, evaluate and execute the matching function
    case "$1" in
        "build")
            build
            ;;
        "push")
            push
            ;;
        "deploy")
            deploy
            ;;
        'help'|'-h'|'--help')
            printHelp
            ;;
        *)
            echo "Invalid parameter. Usage: $0 [build|push|deploy|help]"
            cd "$WORK_DIR"
            exit 1
            ;;
    esac
fi
cd "$WORK_DIR"
