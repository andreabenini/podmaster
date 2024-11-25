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
import pty
import sys
import yaml
import select
import requests
import subprocess


class SystemUtility():
    def __init__(self):
        self.__dryrun = False

    # Current program full path (property)
    @property
    def programPath(self):
        try:
            return os.path.dirname(os.path.realpath(sys.argv[0]))
        except IndexError:
            return os.getcwd()
    # Dry-Run mode, system wide property
    @property
    def dryrun(self):
        return self.__dryrun
    @dryrun.setter
    def dryrun(self, Value):
        self.__dryrun = Value

    # Detect root execution, abort script when detected
    def ForbidRootExecution(self, Message="You cannot run this script as root"):
        if os.geteuid()==0:
            self.Exit(Message)

    # Print a message and ask for confirmation
    def Confirm(self, Message='', Confirm=['y','yes']):
        try:
            if input(Message).lower().strip() in Confirm:
                return True
        except KeyboardInterrupt:
            pass
        return False
    
    # Press any key to continue method
    def Keypress(self, Message='Press any key to continue...'):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            print(Message, end='', flush=True)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

    # Dummy console line available    
    def Line(self, length=80):
        return '-'*length
    def PrintLine(self, length=80):
        print(self.Line(length=length))

    # Program exit with a message
    def Exit(self, Message='', Prepend='ERROR: ', exit=1):
        print(f"\n{Prepend}{Message}\n\n")
        sys.exit(exit)

    # Return a dict with a yaml file loaded in it
    def LoadYAML(self, filename=None):
        try:
            with open(filename, 'r') as fHandler:
                return yaml.safe_load(fHandler)
        except Exception as E:
            print(E)
        return {}

    # Call a method of an object, if it exists (reflection)
    def MethodName(self, object=None, method=None):
        if hasattr(object, method) and callable(getattr(object, method)):   # Get the method from the object
            return getattr(object, method)
        else:
            return None

    # Execute an external program
    # @return (string, string, int) -> (Stdout, StdErr, Return Code)
    def Exec(self, Command='', stdInput=None, printOutput=False, tty=False):
        try:
            if self.dryrun:
                print("[[DRY-RUN]]  "+Command)
                return "", "", 0    # Dry-Run always succeeds but output is always empty
            
            # TTY allocated, read stdout in a totally different way because TTY is allocated, don't use it
            # unless strictly required, process.communicate() is way more painless
            if tty:
                master, slave = pty.openpty()
                process = subprocess.Popen(Command, stdin=slave, stdout=slave, stderr=slave, close_fds=True)
                os.close(slave)
                if stdInput:
                    os.write(master, stdInput.encode())
                stdError = stdOutput = ''
                while process.poll() is None:
                    r, _, _ = select.select([master], [], [], 0.1)
                    if master in r:
                        data = os.read(master, 1024)
                        if not data:  # End of output
                            break
                        # Since stdout and stderr are mixed in the PTY output, 
                        # you'll need a way to distinguish them here.
                        # This might involve analyzing the data or using a more sophisticated approach. 
                        # For now, let's just append all output to stdout:
                        stdOutput += data.decode()

            # Use this method as much as possible (it's fast) and avoid allocating a TTY unless strictly required
            else:
                process = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
                stdOutput, stdError = process.communicate(input=stdInput)
            if printOutput:
                print(f"{stdOutput}\n{stdError}".strip())
            return stdOutput, stdError, process.returncode
        except FileNotFoundError as E:
            return None, str(E), 1    # Return 1 as exit status for command not found
        except KeyboardInterrupt:
            return None, None, 130  # Return 130 as exit status for Ctrl+C


    # Downloads a file from a URL and saves it locally
    def downloadFile(self, url=None, filename=None):
        try:
            response = requests.get(url, stream=True)                   # Send a GET request to the URL
            response.raise_for_status()                                 # Raise an error for HTTP codes 4xx/5xx
            if not hasattr(response, 'iter_content'):
                raise ValueError('invalid response while downloading url, iter_content is null')
            with open(filename, 'wb+') as file:                         # Open the local file in write-binary mode
                for chunk in response.iter_content(chunk_size=8192):    # Download in chunks
                    if chunk:
                        file.write(chunk)
            return (True, "")
        except Exception as e:
            return (False, f"Error while downloading file: {e}")


    # Delete an existing file if present or do not raise errors
    def fileDelete(self, filename):
        try:
            os.remove(filename)
        except:
            return



System = SystemUtility()
