import os
import pandas as pd


class FileManager:
    def __init__(self):
        pass

    def saveFile(self, file_path,fileContent):
        try:
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, 'wb') as file:
                file.write(fileContent)
        except:
            print('Exception in FileManager.saveFile(', file_path)

    def getCSVFileAsPandas(self,file_path):
        # with open(file_path, 'r') as file:
        #     file.read()
        dataFrame = None
        try:
            dataFrame = pd.read_csv(file_path)
        except:
            print('Exception in Loading DataFrame from ', file_path)
        return dataFrame