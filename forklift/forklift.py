#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @description      forklift - Container friendly CLI utility
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              Curses based CLI utility for dealing with local containers
#                   in your favorite local runtime environment (podman, docker)
#
VERSION='0.1'

import os
import sys
try:
    import yaml
    import curses
    import argparse

    from forklift.menu       import Menu
    from forklift.screen     import Screen
    from forklift.confirm    import Confirm
    from forklift.inputBox   import InputBox
    from forklift.container  import Container
    from forklift.messageBox import MessageBox
except Exception as E:
    print(f"Error while importing modules:\n{str(E)}\nAborting program\n\n")
    sys.exit(1)


class ForkliftSystem(object):
    def __init__(self, path=''):
        self.__Exit = False
        self.__editor = os.getenv('EDITOR')
        if not self.__editor: 
            self.__editor = ''
        self.__screen = Screen()
        self.__file_system = path+os.path.sep+'system.yaml'
        self.__menuMain = Menu(screen=self.__screen.screen)
        self.__container = Container(path=path)
        self.__LoadSystemConfig()
        self.__StatusInit()

    def Run(self):
        while not self.__Exit:
            self.__screen.Clear()
            self.__StatusBar()
            if self.__tabCurrent == 1:          # Images tab
                self.__tabImages()
            elif self.__tabCurrent == 2:        # System tab
                self.__tabSystem()
            else:                               # Containers (default) tab
                self.__tabContainers()

    def Close(self):
        self.__screen.close()

    def __LoadSystemConfig(self):
        try:
            if not self.__ReloadSystemConfig():
                with open(self.__file_system, 'w+') as file:            # Fill up with default values
                    yaml.dump({'container': 'podman'}, file)
                self.__ReloadSystemConfig()
        except Exception as E:
            MessageBox(title='E R R O R', message=f'\n\nCannot create configuration file \n{self.__file_system}\n\n\nClosing Application\n\n',
                       footer=' press any key to continue ', x=1, y=1, colors=(curses.COLOR_WHITE, curses.COLOR_RED))
            self.__Exit = True

    def __ReloadSystemConfig(self):
        try:
            with open(self.__file_system, 'r') as file:
                self.__systemInformation = yaml.safe_load(file)
                self.__container.platform = self.__systemInformation['container']
                return True
        except Exception as E:
            self.__systemInformation = {}
        return False


    def __editFile(self, filename=None):
        if self.__editor == '' or not filename:
            MessageBox(title='E R R O R', message=f'\n\n System variable $EDITOR is not set \n    Check SYSTEM TAB for details\n\n',
                        footer=' press any key to continue ', x=10, y=10, colors=(curses.COLOR_WHITE, curses.COLOR_RED))
            return
        self.__screen.Exec(f"{self.__editor} '{filename}'")

    def __newContainer(self):
        containers = self.__container.containerProfilesList()
        menuNewContainer = Menu(screen=self.__screen.screen, colors=(curses.COLOR_WHITE, curses.COLOR_BLUE))
        for key,_ in containers:
            menuNewContainer.itemAdd(key)
        menuNewContainer.itemAdd("<<--         Manual Input         -->>")
        menuNewContainer.itemAdd("<<--     Edit containers.yaml     -->>")
        MessageBox(title='Current directory', message='\n '+str(os.getcwd())+'\n'+(' '*42)+'\n', x=21, y=2, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK), height=15, keypress=False)
        selection = menuNewContainer.Display(X=24, Y=6, caption='Create new container from image', lines=10, itemWidth=40, footer='<ESC>.Cancel')
        if selection == -1:                                                 # Abort
            return
        elif selection == len(menuNewContainer.items)-1:                    # Edit containers.yaml file
            self.__editFile(self.__container.filecontainers)
            self.__container.LoadContainers()
            return
        elif selection == len(menuNewContainer.items)-2:                    # Free manual input
            value = self.__container.platform+' run --hostname HOSTNAMEHERE --name NAME -it IMAGENAME /bin/bash'
        else:
            value = list(containers)[selection][1]
        # Edit parameters before executing them
        cliCommand = InputBox(defaultValue=value, title='Input parameters for container creation (edit and adapt your own)', footer2=os.getcwd(), 
                              size=1024, colors=(curses.COLOR_BLACK, curses.COLOR_CYAN), footer='<ENTER>.Confirm <ESC>.Cancel')
        # Pause curses and execute command
        if cliCommand.value:
            self.__screen.Exec(cliCommand.value)

    def __newImage(self):
        images = self.__container.imageProfilesList()
        menuNewImage = Menu(screen=self.__screen.screen, colors=(curses.COLOR_WHITE, curses.COLOR_BLUE))
        for key,_ in images:
            menuNewImage.itemAdd(key)
        menuNewImage.itemAdd("<<--         Manual Input         -->>")
        menuNewImage.itemAdd("<<--       Edit images.yaml       -->>")
        MessageBox(title='Current directory', message='\n '+str(os.getcwd())+'\n'+(' '*42)+'\n', x=21, y=2, colors=(curses.COLOR_WHITE, curses.COLOR_BLACK), height=15, keypress=False)
        selection = menuNewImage.Display(X=24, Y=6, caption='Create new image from profile', lines=10, itemWidth=40, footer='<ESC>.Cancel')
        if selection == -1:                                                 # Abort
            return
        elif selection == len(menuNewImage.items)-1:                        # Edit images.yaml file
            self.__editFile(self.__container.fileimages)
            self.__container.LoadImages()
            return
        elif selection == len(menuNewImage.items)-2:                        # Free manual input
            value = self.__container.platform+' build -t IMAGENAME_HERE CONTAINERFILE_NAME'
        else:
            value = list(images)[selection][1]
        # Edit parameters before executing them
        cliCommand = InputBox(defaultValue=value, title='Input parameters for image creation (edit and adapt your own)', footer2=os.getcwd(),
                              size=1024, colors=(curses.COLOR_BLACK, curses.COLOR_CYAN), footer='<ENTER>.Confirm <ESC>.Cancel')
        # Pause curses and execute command
        if cliCommand.value:
            cliExecCommand = cliCommand.value + '; echo -en "\n\nPress any key to continue..."; read -n 1 junk'
            self.__screen.Exec(cliExecCommand)


    def __editContainer(self, containerID):
        menu = []
        menu.append((' Start - Attach', 'start'))
        menu.append((' Stop', 'stop'))
        menu.append((' Kill', 'kill'))
        menu.append((' Rename', 'rename'))
        menu.append((' Remove', 'remove'))
        (_, ID, Name, Status) = containerID
        menuAction = Menu(screen=self.__screen.screen, colors=(curses.COLOR_WHITE, curses.COLOR_BLUE))
        menuAction.items = menu
        selected = menuAction.Display(caption=f"[{Name}]", footer=f'Status: {Status}', itemWidth=30, lines=7, X=20, Y=8)
        if selected==-1:
            return
        (_, action) = menu[selected]
        if   action=='start':
            self.__screen.Exec(self.__container.platform+' start -ai '+ID)
            return
        elif action=='stop':
            message = str(self.__container.Stop(containerID=ID))
            title = f'Stopping {Name}'
        elif action=='kill':
            message = str(self.__container.Kill(containerID=ID))
            title = f'Killing in the name of [{Name}]'
        elif action=='rename':
            nameNew = InputBox(defaultValue=Name, title=f'New name for "{Name}"', size=100, colors=(curses.COLOR_BLACK, curses.COLOR_CYAN), footer='<ENTER>.Confirm <ESC>.Cancel', y=10)
            if nameNew.value:
                if self.__container.Rename(ID, nameNew.value) != '':
                    MessageBox(title='E R R O R', message=f'\n\nCannot rename\n"{ID}"\nas "{nameNew.value}"\n\n', footer=' press any key to continue ', x=1, y=1, colors=(curses.COLOR_WHITE, curses.COLOR_RED))
                    return
                message = f"New name: '{nameNew.value}'\n                 "
                title = 'Container Renamed'
            else:
                return
        elif action=='remove':
            confirm = Confirm(f"\nDelete container            \n'{Name}'\n", title="Confirm Container Deletion ?", colors=(curses.COLOR_BLACK, curses.COLOR_YELLOW), messageButtons=[' Yes ', ' No '], messageSelected=1, screen=self.__screen.screen)
            if confirm.value == 0:
                message = str(self.__container.Remove(containerID=ID))
                title = f'Removing {Name}'
            else:
                return
        else:
            return
        MessageBox(title=title, message=f'\n{message}\n', footer='press any key...', x=10, y=10, colors=(curses.COLOR_WHITE, curses.COLOR_CYAN))

    def __StatusInit(self):
        self.__statusBarPages = [(' Containers'), ('   Images'), ('   System')]
        self.__tabCurrent  = 0
        self.__statusBarActive   = self.__screen.newUUID()
        self.__statusBarInactive = self.__screen.newUUID()
        curses.start_color()
        curses.init_pair(self.__statusBarActive,   curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(self.__statusBarInactive, curses.COLOR_BLACK, curses.COLOR_BLUE)

    def __StatusBar(self):                                                  # Just a stub, not implemented yet
        xPos = 0
        self.__screen.Text(Caption='\u2191\u2193\u2190\u2192 to navigate', X=64, Y=0)
        for index, item in enumerate(self.__statusBarPages):
            (name) = item
            activeColor = self.__statusBarActive if index==self.__tabCurrent else self.__statusBarInactive
            window = curses.newwin(1, 18, 0, xPos)
            window.bkgd(curses.color_pair(activeColor))
            window.addstr(0, 3, name)
            window.refresh()
            xPos += 20

    def __tabContainers(self):
        (menuItems, labelFormat) = self.__container.List()
        menuItems.append(('< Create New Container >', ''))
        self.__menuMain.items = menuItems
        self.__screen.Text(Caption=labelFormat.format(id='UID', image='Image Name', name='Container Name', state='Status', createdAt='Created At', command='Shell'), X=5, Y=2)
        selection = self.__menuMain.Display(X=5, Y=3, keys=[curses.KEY_RIGHT])
        if selection == -1:                                                 # <esc>: just reload the container list
            pass
        elif selection == -2:                                               # Tab: Images
            self.__tabCurrent = 1
        elif selection == len(menuItems)-1:                                 # New
            self.__newContainer()
        else:                                                               # Existing container, action upon it
            self.__editContainer(menuItems[selection])

    def __tabImages(self):
        imagesMenu = Menu(screen=self.__screen.screen)
        (imagesMenuItems, labelFormat) = self.__container.imagesList()
        imagesMenuItems.append(('< Create New Image >', 'newimage', ''))
        imagesMenu.items = imagesMenuItems
        labelTitle = labelFormat.format(repository='REPOSITORY', tag='TAG', id='IMAGE ID', created='CREATED', size='SIZE')
        self.__screen.Text(Caption=labelTitle, X=5, Y=2)
        selection = imagesMenu.Display(X=5, Y=3, keys=[curses.KEY_LEFT, curses.KEY_RIGHT])
        if selection == -1:                                                 # <Escape>
            pass
        elif selection == -2:                                               # <Left>
            self.__tabCurrent = 0
        elif selection == -3:                                               # <Right>
            self.__tabCurrent = 2
        elif selection == len(imagesMenuItems)-1:
            self.__newImage()
        else:
            (_, ID, name) = imagesMenuItems[selection]
            self.__tabImagesItemMenu(ID=ID, name=name)

    def __tabImagesItemMenu(self, ID=None, name=''):
        if not ID:
            return
        menuAction = Menu(screen=self.__screen.screen, colors=(curses.COLOR_WHITE, curses.COLOR_BLUE))
        menuAction.items = [
            (f'Rename "{name}"', 'rename'),
            (f'Remove "{name}"', 'remove'),
        ]
        selected = menuAction.Display(caption=f"[{ID}]", footer=' Images action menu  <ESC>.Exit ', itemWidth=70, lines=7, X=20, Y=8)
        if selected == -1:
            return
        elif selected == 0:
            imageNewName = InputBox(title='Enter the new name for the image', size=1024, colors=(curses.COLOR_BLACK, curses.COLOR_CYAN), footer='<ENTER>.Confirm <ESC>.Cancel', y=10)
            if imageNewName.value:
                newName = imageNewName.value.replace(' ', '')       # Removing spaces, if any
                result = self.__container.imageRename(imageIDOld=ID, imageNameNew=newName)
                if result.strip() != '':
                    MessageBox(title='E R R O R', message=f'\n{result.strip()}\n', footer=' press any key to continue ', y=12, colors=(curses.COLOR_WHITE, curses.COLOR_RED))
        elif selected == 1:
            result = Confirm(f"\nDelete image            \n'{ID}'\n", title="Confirm Image Deletion ?", colors=(curses.COLOR_BLACK, curses.COLOR_YELLOW), messageButtons=[' Yes ', ' No '], messageSelected=1, screen=self.__screen.screen)
            if result.value == 0:
                self.__container.imageDelete(imageID=ID)

    def __tabSystem(self):
        self.__screen.Text(Caption=f'Forklift version      v{VERSION}', X=5, Y=2)
        self.__screen.Text(Caption=f'System environment    $EDITOR variable is '+('set' if self.__editor!='' else 'not set'), X=5, Y=4)
        self.__screen.Text(Caption=f'Program $EDITOR       "{self.__editor}"', X=5, Y=5)
        self.__screen.Text(Caption=f'Container runtime     "{self.__container.platform}"', X=5, Y=6)

        systemMenu = Menu(screen=self.__screen.screen)
        systemMenu.items = [
            ('Edit program configuration       <system.yaml>',     'config'),
            ('Edit container build profiles    <containers.yaml>', 'containers'),
            ('Edit image build profiles        <images.yaml>',     'images'),
            ('Exit Program', 'exit'),
        ]
        selection = systemMenu.Display(X=5, Y=9, keys=[curses.KEY_LEFT])
        if selection == -1:             # Escape, reload menu
            pass
        elif selection == -2:           # Left (goto tab left)
            self.__tabCurrent = 1
        elif selection == 0:            # Edit system.yaml
            self.__editFile(self.__file_system)
            self.__ReloadSystemConfig()
        elif selection == 1:            # Edit containers.yaml
            self.__editFile(self.__container.filecontainers)
            self.__container.LoadContainers()
        elif selection == 2:            # Edit images.yaml
            self.__editFile(self.__container.fileimages)
            self.__container.LoadImages()
        elif selection == 3:            # Exit
            self.__Exit = True            


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Forklift: friendly utility for dealing with containers', epilog=f" ", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-p', '--path',  dest='path',  default=os.path.dirname(os.path.realpath(__file__)),  help=f"System and user configuration files path (default: {os.path.dirname(os.path.realpath(__file__))})")
    argument = parser.parse_args()
    App = ForkliftSystem(path=argument.path)
    App.Run()
    App.Close()
