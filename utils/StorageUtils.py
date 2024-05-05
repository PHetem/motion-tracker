import os
import config.Config as Config

class StorageUtils:

    directory = None

    def __init__(self, directory):
        self.directory = directory

    def manageStorageSpace(self):
        if not self.hasStorageSpace():
            self.cleanUp()

    def hasStorageSpace(self):
        occupied = sum(file.stat().st_size for file in os.scandir(self.directory) if file.is_file())
        return occupied < Config.conf['storageLimit']

    def cleanUp(self):
        print('cleaning up older files')
        # Get visible files
        fileList = [file for file in os.listdir(self.directory) if not self.is_hidden(file)]

        # Add directory to path
        fileList = [self.directory + "/{0}".format(file) for file in fileList]

        # Sort files by date
        fileList.sort(key = os.path.getctime)

        while not self.hasStorageSpace():
            os.remove(os.path.abspath(fileList[0]))
            fileList.pop(0)
            print('removed file ' + fileList[0])

    def is_hidden(self, file):
        return file.startswith('.')


