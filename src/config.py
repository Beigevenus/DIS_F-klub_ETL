import configparser
from pathlib import Path
import os

class Config:
    def __init__(self, file_name="config.ini", 
                 config_file_dir=str(Path(__file__).parent)):
        self._conf_obj = configparser.ConfigParser()

        ini_path = os.path.join(config_file_dir, file_name)
        self._conf_obj.read(ini_path)

    @property
    def _data_folder_name(self):
        return self._conf_obj["FolderNames"]

    @property
    def _file_names(self):
        return self._conf_obj["FileNames"]

    @property
    def data_folder_name(self):
        return self._data_folder_name["DataFolderName"]

    @property
    def file_name_category(self):
        return self._file_names["Category"]

    @property
    def file_name_members(self):
        return self._file_names["Members"]

    @property
    def file_name_product_categories(self):
        return self._file_names["ProductCategories"]

    @property
    def file_name_product(self):
        return self._file_names["Product"]

    @property
    def file_name_room(self):
        return self._file_names["Room"]

    @property
    def file_name_sale(self):
        return self._file_names["Sale"]




if __name__ == "__main__":
    config = Config()
    print(config)

