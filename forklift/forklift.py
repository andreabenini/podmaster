#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @description      forklift - Container friendly CLI utility
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              CLI/GUI utility for dealing with local containers
#                   in your favorite local runtime environment (podman, docker)
#
# pyright: reportMissingImports=false
#
VERSION='1.0.1'
CODENAME='Cthulhu'

import os
import sys
try:
    import argparse
    import subprocess

    from forkliftlib            import bless
    from forkliftlib.container  import Container
except Exception as E:
    print(f"Error while importing modules:\n{str(E)}\nAborting program\n\n")
    sys.exit(1)
MSG_ANY_KEY=' press any key... '
COLOR=(bless.WHITE, bless.BLUE)

class ForkliftSystem(object):
    def __init__(self, path=''):
        self.__Exit = False
        self.__editor = os.getenv('EDITOR')
        if not self.__editor: 
            self.__editor = ''
        self.__screen = bless.bless(init=True)
        self.__container = Container(path=path)
        self.__StatusInit()

    def Run(self):
        if not self.__container.valid:
            self.__screen.messageBox(Title='E R R O R', Message='\n\nCannot detect container engine\nCurrently supporting: ('+"|".join(self.__container.platformList)+')\n\nClosing Application\n\n', Footer=MSG_ANY_KEY, Color=(bless.WHITE, bless.RED))
            return
        while not self.__Exit:
            self.__screen.clear()
            self.__StatusBar()
            if self.__tabCurrent == 1:          # Images tab
                self.__tabImages()
            elif self.__tabCurrent == 2:        # System tab
                self.__tabSystem()
            else:                               # Containers (default) tab
                self.__tabContainers()

    def Close(self):
        self.__screen.clear()
        self.__screen.close()

    def __editFile(self, filename=None):
        if self.__editor == '' or not filename:
            self.__screen.messageBox(Title='E R R O R',  Message=f'\n\n System variable $EDITOR is not set \n    Check [System] tab for details\n\n', Footer=MSG_ANY_KEY, Color=(bless.WHITE, bless.RED))
            return
        self.__exec(Command=f"{self.__editor} '{filename}'")

    def __exec(self, Command=''):
        self.__screen.pause()
        result = subprocess.run(Command, shell=True)
        self.__screen.restore()
        return result.returncode

    def __containerNew(self):
        cwdMessage = '\n'+str(os.getcwd())+'\n'+(' '*42)+'\n'
        menuSize   = self.__screen.textGetColMax(cwdMessage)
        menu = self.__screen.menu(Color=COLOR)
        containers = self.__container.containerProfilesList()
        for key,_ in containers:
            menu.itemAdd(key)
        menu.itemAdd("<<---"+self.__screen.textCenter(Text="Manual Input",         Size=menuSize-12)+"--->>")
        menu.itemAdd("<<---"+self.__screen.textCenter(Text="Edit containers.yaml", Size=menuSize-12)+"--->>")
        self.__screen.messageBox(Title='Current directory', Message=cwdMessage, X=15, Y=4, Color=(bless.WHITE, bless.BLACK), Height=15, Keypress=False)
        selection = menu.Display(X=17, Y=8, Caption='Create new container from image', Lines=10, ItemWidth=menuSize, Footer="<ESC>.Cancel")
        if selection == -1:                                         # <esc> Abort
            return
        elif selection == len(menu.items)-1:                        # Edit containers.yaml file
            self.__editFile(self.__container.filecontainers)
            self.__container.LoadContainers()
            return
        if selection == len(menu.items)-2:                          # Free manual input (suggested input)
            value = self.__container.platform+' run --hostname HOSTNAMEHERE --name NAME -it IMAGENAME /bin/bash'
        else:
            value = list(containers)[selection][1]                  # Command to execute from the list
        # Edit parameters before executing them (msgbox below just for drawing user attention)
        self.__screen.messageBox(Width=self.__screen.cols, Height=1024//(self.__screen.cols-2)+7, Y=13, X=1, Color=(bless.WHITE, bless.BLACK), Keypress=False)
        cliCommand = self.__screen.editBox(Title='Input parameters for container creation (edit and adapt your own)', Color=COLOR, Footer2=os.getcwd(),
                                           DefaultValue=value, Y=15, Size=1024, Width=self.__screen.cols-2, Footer='<ENTER>.Confirm <ESC>.Cancel')
        if cliCommand.value:                                        # UI on hold and execute command
            self.__exec(Command=cliCommand.value)

    def __containerEdit(self, containerID):
        (_, ID, Name, Status) = containerID
        colors = COLOR
        menu = self.__screen.menu(Color=COLOR, Items=[
                (' Start - Attach', 'start'),
                (' Stop',           'stop'),
                (' Kill',           'kill'),
                (' Logs',           'log'),
                (' Rename',         'rename'),
                (' Remove',         'remove'),
        ])
        menu.itemAdd((" <<---"+self.__screen.textCenter(Text="[[ custom action ]]", Size=68-12)+"--->>", 'custom'))    # Empirically bigger than first option
        selection = menu.Display(Caption=f"[{Name}]", Footer=f'Status: {Status}', ItemWidth=70, Lines=9, X=10, Y=8)
        if selection==-1:
            return
        (_, action) = menu.items[selection]
        if action == 'custom':                        # custom action, suggesting attach as a sample
            userAction = self.__screen.editBox(Title=f'custom action to execute', Footer='<ENTER>.Confirm <ESC>.Cancel', Size=200, Y=10,
                                               DefaultValue=self.__container.platform+f' exec -it {ID} /bin/bash')
            if userAction.value:
                self.__exec(Command=userAction.value)
            return
        elif action=='log':
            self.__exec(Command=self.__container.cmdLog(containerID=ID))
            return
        elif action=='start':
            # Start
            if Status.lower() != 'running':
                self.__exec(Command=self.__container.cmdStart(containerID=ID))
                return
            # Attach
            for guessedShell in self.__container.containerShellList:
                result = self.__exec(Command=self.__container.cmdAttach(containerID=ID)+' '+guessedShell)
                if result == 0:
                    return
            self.__screen.messageBox(Title='E R R O R', Message=f'\nCannot detect a suitable shell for attaching to this container\n[{", ".join(self.__container.containerShellList)}]\n\n{ID}\n', Footer=MSG_ANY_KEY, Color=(bless.WHITE, bless.RED))
            return
        elif action=='stop':
            title = f'Stopping {Name}'
            message = self.__container.Stop(containerID=ID)
        elif action=='kill':
            title = f'Killing in the name of [{Name}]'
            message = self.__screen.textWrap(Text=self.__container.Kill(containerID=ID), Max=60)
        elif action=='rename':
            nameNew = self.__screen.editBox(Title=f'New name for "{Name}"', Footer='<ENTER>.Confirm <ESC>.Cancel', Size=100, DefaultValue=Name, Y=10)
            if nameNew.value:
                if self.__container.Rename(ID, nameNew.value) != '':
                    title   = 'E R R O R'
                    colors  = (bless.WHITE, bless.RED)
                    message = f'\nCannot rename\n"{ID}"\nas "{nameNew.value}"\n'
                else:
                    title   = 'Container Renamed'
                    message = f'New name: "{nameNew.value}"\n'+(' '*18)
            else:
                return
        elif action=='remove':
            confirm = self.__screen.confirmBox(Title="Confirm Container Deletion", Message=f"\nDelete container            \n'{Name}'\n", 
                                               Color=(bless.BLACK, bless.YELLOW), MessageButtons=[' Yes ', ' No '], ButtonSelected=1)
            if confirm == 0:
                (returnCode, message) = self.__container.Remove(containerID=ID)
                if returnCode == 0:
                    title   = 'Removing '+Name
                else:
                    title   = 'E R R O R'
                    colors  = (bless.WHITE, bless.RED)
                    message = self.__screen.textWrap(Text=message, Max=60)
            else:
                return
        else:
            return
        self.__screen.messageBox(Title=title, Message=f'\n{message}\n', Footer=MSG_ANY_KEY, Color=colors)

    def __imageNew(self):
        cwdMessage = '\n'+str(os.getcwd())+'\n'+(' '*42)+'\n'
        menuSize   = self.__screen.textGetColMax(cwdMessage)
        menu = self.__screen.menu(Color=COLOR)
        images = self.__container.imageProfilesList()
        for key,_ in images:
            menu.itemAdd(key)
        menu.itemAdd("<<---"+self.__screen.textCenter(Text="Manual Input",     Size=menuSize-12)+"--->>")
        menu.itemAdd("<<---"+self.__screen.textCenter(Text="Edit images.yaml", Size=menuSize-12)+"--->>")
        self.__screen.messageBox(Title='Current directory', Message=cwdMessage, X=19, Y=4, Color=(bless.WHITE, bless.BLACK), Height=15, Keypress=False)
        selection = menu.Display(X=21, Y=8, Caption='Create new image from profile', Lines=10, ItemWidth=menuSize, Footer='<ESC>.Cancel')
        if selection == -1:                                         # Abort
            return
        elif selection == len(menu.items)-1:                        # Edit images.yaml file
            self.__editFile(self.__container.fileimages)
            self.__container.LoadImages()
            return
        elif selection == len(menu.items)-2:                        # Free manual input
            value = self.__container.platform+' build -t IMAGENAME_HERE CONTAINERFILE_DIR'
        else:
            value = list(images)[selection][1]
        # Edit parameters before executing them
        self.__screen.messageBox(Width=self.__screen.cols, Height=512//(self.__screen.cols-2)+7, Y=13, X=1, Color=(bless.WHITE, bless.BLACK), Keypress=False)
        cliCommand = self.__screen.editBox(Title='Input parameters for image creation (edit and adapt your own)', Color=COLOR, Footer2=os.getcwd(),
                                           DefaultValue=value, Y=15, Size=512, Width=self.__screen.cols-2, Footer='<ENTER>.Confirm <ESC>.Cancel')
        if cliCommand.value:                                        # UI on hold and execute command
            self.__exec(cliCommand.value+'; echo -en "\n\nPress any key to continue..."; read -n 1 junk')

    def __imageEdit(self, ID=None, name=''):
        if not ID:
            return
        colors = COLOR
        menu = self.__screen.menu(Color=colors, Items=[
                (f'Rename "{name}"', 'rename'),
                (f'Remove "{name}"', 'remove'),
        ])
        selection = menu.Display(Caption=f"[{ID}]", Footer=' Images action menu  <ESC>.Exit ', ItemWidth=70, Lines=7, X=10, Y=8)
        if selection == -1:
            return
        elif selection == 0:                                    # Rename
            imageNew = self.__screen.editBox(Title='New name for the image', Footer='<ENTER>.Confirm <ESC>.Cancel', Size=100, DefaultValue=name, Y=10)
            if imageNew.value:
                newName = imageNew.value.replace(' ', '')       # Removing spaces, if any
                if self.__container.imageRename(imageIDOld=ID, imageNameNew=newName) != '':
                    title ='E R R O R'
                    colors = (bless.WHITE, bless.RED)
                    message = f'\nCannot rename\n"{ID}"\nas "{newName}".\n'
                else:
                    title='Image Renamed'
                    message=f'New name: \n"{newName}"\n'+(' '*18)
            else:
                return
        elif selection == 1:                                    # Remove
            confirm = self.__screen.confirmBox(Title="Confirm Image Deletion", Message=f"\nDelete image            \n'{ID}'\n",
                                               Color=(bless.BLACK, bless.YELLOW), MessageButtons=[' Yes ', ' No '], ButtonSelected=1)
            if confirm == 0:
                (returnCode, message) = self.__container.imageRemove(imageID=ID)
                if returnCode == 0:
                    title=f'Removing {name}'
                else:
                    title   = 'E R R O R'
                    colors  = (bless.WHITE, bless.RED)
                    message = self.__screen.textWrap(Text=message, Max=60)
            else:
                return
        else:
            return
        self.__screen.messageBox(Title=title, Message=f'\n{message}\n', Footer=MSG_ANY_KEY, Color=colors)

    def __StatusInit(self):
        self.__tabCurrent  = 0
        self.__statusBarPages = [('Containers'), ('Images'), ('System')]

    def __StatusBar(self):
        xPos = 1
        size = 16
        self.__screen.text(Text='\u2191\u2193\u2190\u2192 to navigate', X=56, Y=1)
        for index, item in enumerate(self.__statusBarPages):
            (name) = item
            color = (bless.BLACK, bless.WHITE) if index==self.__tabCurrent else (bless.BLACK, bless.BLUE)
            self.__screen.label(name, Size=size, Color=color, Center=True, X=xPos)
            xPos += size+2

    def __tabContainers(self):
        menu = self.__screen.menu()
        (menuItems, labelFormat) = self.__container.List()
        menuItems.append(('< Create New Container >', ''))
        menu.items = menuItems
        self.__screen.text(Text=labelFormat.format(id='UID', image='Image Name', name='Name', state='Status', createdAt='Created At', command='Shell'), X=3, Y=3)
        selection = menu.Display(X=3, Y=4, Keys=['RIGHT'])
        if selection == -1:                                                 # <esc>: just reload the container list
            pass
        elif selection == -2:                                               # Tab: Images
            self.__tabCurrent = 1
        elif selection == len(menuItems)-1:                                 # New container
            self.__containerNew()
        else:                                                               # Existing container, action on it
            self.__containerEdit(menuItems[selection])

    def __tabImages(self):
        menu = self.__screen.menu()
        (menuItems, labelFormat) = self.__container.imagesList()
        menuItems.append(('< Create New Image >', 'newimage', ''))
        menu.items = menuItems
        self.__screen.text(Text=labelFormat.format(repository='REPOSITORY', tag='TAG', id='IMAGE ID', created='CREATED', size='SIZE Mb'), X=3, Y=3)
        selection = menu.Display(X=3, Y=4, Keys=['LEFT', 'RIGHT'])
        if selection == -1:                                                 # <Escape>
            pass
        elif selection == -2:                                               # <Left>
            self.__tabCurrent = 0
        elif selection == -3:                                               # <Right>
            self.__tabCurrent = 2
        elif selection == len(menuItems)-1:
            self.__imageNew()
        else:
            (_, ID, name) = menuItems[selection]
            self.__imageEdit(ID=ID, name=name)

    def __tabSystem(self):
        self.__screen.text(Text=f'Forklift v              '+'"'*(len(CODENAME)+2), X=6, Y=3)
        self.__screen.text(Text=VERSION,  X=16, Y=3, Color=(bless.CYAN,   (1,1)))
        self.__screen.text(Text=CODENAME, X=31, Y=3, Color=(bless.YELLOW, (1,1)))
        self.__screen.text(Text=f'System environment      $EDITOR variable is '+('set' if self.__editor!='' else 'not set'), X=6, Y=5)
        self.__screen.text(Text=f'Program $EDITOR         "{self.__editor}"', X=6, Y=6)
        self.__screen.text(Text=f'Container runtime       "{self.__container.platform}"', X=6, Y=7)
        menu = self.__screen.menu(Items=[
            ('Edit container build profiles    <containers.yaml>', 'containers'),
            ('Edit image build profiles        <images.yaml>',     'images'),
            ('Exit Program', 'exit'),
        ])
        selection = menu.Display(X=6, Y=10, Keys=["LEFT"])
        if selection == -1:             # Escape, reload menu
            pass
        elif selection == -2:           # Left (goto tab left)
            self.__tabCurrent = 1
        elif selection == 0:            # Edit containers.yaml
            self.__editFile(self.__container.filecontainers)
            self.__container.LoadContainers()
        elif selection == 1:            # Edit images.yaml
            self.__editFile(self.__container.fileimages)
            self.__container.LoadImages()
        elif selection == 2:            # Exit
            self.__Exit = True

def main():                             # Entry point for the package (when installed from pip)
    pathDefault = os.path.dirname(os.path.realpath(__file__+os.path.sep+'..' if __file__.endswith('__main__.py') else __file__))
    parser = argparse.ArgumentParser(description='Forklift: friendly utility for dealing with containers', epilog=f" ", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--path',  dest='path',  default=pathDefault,  help=f"System and user configuration files path (default: {pathDefault})")
    argument = parser.parse_args()
    App = ForkliftSystem(path=argument.path)
    App.Run()
    App.Close()

if __name__ == "__main__":
    main()
