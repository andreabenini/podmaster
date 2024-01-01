#!/usr/bin/env sh
#
# Execute forklift on a remote host through SSH connection
#   - Copy application on remote host
#   - Execute program there through the ssh connection
#   - Delete the app once done
#

# Adapt these to your environment
APP_NAME=forklift.app
REMOTE_USER=ben@hostname
REMOTE_PATH=.
REMOTE_EDITOR=`which vim`

# authorized_keys filename helps a lot if you want to avoid typing passwords all the time
scp $APP_NAME $REMOTE_USER:$REMOTE_PATH
ssh -tt $REMOTE_USER "EDITOR=$REMOTE_EDITOR $REMOTE_PATH/$APP_NAME; rm $REMOTE_PATH/$APP_NAME"
