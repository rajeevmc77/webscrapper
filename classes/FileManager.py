import os
import pandas as pd
import string


class FileManager:
    def __init__(self):
        pass

    def saveFile(self, file_path,fileContent):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'wb') as file:
            file.write(fileContent)

    def getCSVFileAsPandas(self,file_path):
        # with open(file_path, 'r') as file:
        #     file.read()
        return pd.read_csv(file_path)