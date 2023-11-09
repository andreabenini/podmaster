# -*- coding: utf-8 -*-
#
# @description      container management class
#
# @author           Andrea Benini
# @date             2023-11-07
# @license          GNU Affero General Public License v3.0
# @see              Containers and images class for dealing with basic operations (list, stop, remove, kill, ...)
#
import math
import os
import yaml
import json
import subprocess

from forkliftlib.menu     import Menu
from forkliftlib.inputBox import InputBox


class Container(object):
    def __init__(self, path='', platform='podman'):
        self.__platform = platform
        self.__file_containers = path+os.path.sep+'containers.yaml'
        self.__file_images     = path+os.path.sep+'images.yaml'
        self.LoadContainers()
        self.LoadImages()

    @property
    def platform(self):
        return self.__platform
    @platform.setter
    def platform(self, value):
        self.__platform = value
    
    @property
    def filecontainers(self):
        return self.__file_containers
    @property
    def fileimages(self):
        return self.__file_images
    
    def __exec(self, command=None):
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True, universal_newlines=True)
            output, _ = process.communicate()
            return (process.returncode, output)
        except subprocess.CalledProcessError as E:
            return (-1, str(E))
    
    def LoadContainers(self):
        try:
            with open(self.__file_containers, 'r') as file:
                self.__containerProfiles = yaml.safe_load(file)
        except Exception as E:
            self.__containerProfiles = {}

    def LoadImages(self):
        try:
            with open(self.__file_images, 'r') as file:
                self.__imageProfiles = yaml.safe_load(file)
        except Exception as E:
            self.__imageProfiles = {}

    def List(self):
        results = []
        (errorCode, output) = self.__exec(f"{self.__platform} ps -a --format=json")
        if errorCode != 0 :
            return results
        jsonData = json.loads(output)
        items = {}
        lenImage = lenName = 0
        for item in jsonData:
            if 'Names' in item and len(item['Names'])>0:
                for itemName in item['Names']:
                    if len(item['Image']) > lenImage:
                        lenImage = len(item['Image'])
                    if len(itemName) > lenName:
                        lenName = len(itemName)
                    items[itemName] = {
                        'id': item['Id'],
                        'idshort': item['Id'][:12],
                        'image': item['Image'],
                        'name': itemName,
                        'state': item['State'],
                        'createdat': item['CreatedAt'],
                        'command': item['Command'][0][:20]
                    }
        formatFields = f"{{id:<12}}  {{image:<{lenImage}}}  {{name:<{lenName}}}  {{state:<7}}  {{createdAt:<20}} {{command}}"
        for item in items:
            label = formatFields.format(
                        id        = items[item]['idshort'],
                        image     = items[item]['image'],
                        name      = items[item]['name'],
                        state     = items[item]['state'],
                        createdAt = items[item]['createdat'],
                        command   = items[item]['command']
            )
            results.append((label, items[item]['id'], items[item]['name'], items[item]['state']))
        return (results, formatFields)


    def Stop(self, containerID=None):
        (_, output) = self.__exec(f"{self.__platform} stop {containerID}")
        return output.strip()

    def Kill(self, containerID=None):
        (_, output) = self.__exec(f"{self.__platform} kill {containerID} 2>&1")
        return output.strip()

    def Rename(self, containerID=None, nameNew=None):
        (_, output) = self.__exec(f"{self.__platform} rename {containerID} {nameNew}")
        return output.strip()

    def Remove(self, containerID=None):
        (_, output) = self.__exec(f"{self.__platform} rm {containerID}")
        return output.strip()

    def containerProfilesList(self):
        return self.__containerProfiles.items()


    def imageProfilesList(self):
        return self.__imageProfiles.items()

    def imagesList(self):
        (errorCode, output) = self.__exec(f"{self.__platform} images -a --format=json")
        if errorCode != 0:
            return []
        jsonData = json.loads(output)
        lenRepository = lenTag = 0
        items = {}
        for item in jsonData:
            repository = tag = '<none>'
            if 'Names' in item and len(item['Names'])>0:
                for itemName in item['Names']:
                    if len(itemName.split(":")) >= 2:
                        [repository, tag] = itemName.split(":")
                    if len(repository) > lenRepository:
                        lenRepository = len(repository)
                    if len(tag) > lenTag:
                        lenTag = len(tag)
                    [created, _] = item['CreatedAt'].split("T")
                    size = math.floor(item['Size']/1000000)
                    items[itemName] = {'idShort': item['Id'][:12], 'repository': repository, 'tag': tag, 'created': created, 'size': size}
        results = []
        formatFields = f"{{repository:<{lenRepository}}}  {{tag:<{lenTag}}}  {{id:12}}  {{created:10}}  {{size}}"
        for item in items:
            label = formatFields.format(
                        repository=items[item]['repository'],
                        tag = items[item]['tag'],
                        id = items[item]['idShort'],
                        created = items[item]['created'],
                        size = str(items[item]['size'])+' MB',
            )
            results.append((label, item, items[item]['repository']))
        return (results, formatFields)

    def imageRename(self, imageIDOld=None, imageNameNew=None):
        if not imageIDOld:
            return ''
        (_, output) = self.__exec(f"{self.__platform} tag '{imageIDOld}' '{imageNameNew}' 2>&1")
        if output.strip()=='':
            self.imageDelete(imageID=imageIDOld)                # I'm not interested in output message like: 'Untagged: ...'
            return ''
        return output.strip()

    def imageDelete(self, imageID=None):
        if not imageID:
            return ''
        (_, output) = self.__exec(f"{self.__platform} rmi {imageID} 2>&1")
        return output.strip()
