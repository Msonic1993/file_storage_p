import os
from datetime import datetime
from os import path

from configuration import UPLOAD_FOLDER
from md5change import md5


class Manage:

    def directorymanager(self):
        access = 0o777
        today = datetime.now()
        pathyear = os.path.join(UPLOAD_FOLDER, str(today.year))
        pathmonth = os.path.join(pathyear, str(today.month))

        try:

            os.makedirs(pathyear, mode=access, exist_ok=False)
            print("Directory ", pathyear, " Created ")

        except FileExistsError:
            print("Directory ", pathyear, " already exists")

        try:
            os.makedirs(pathmonth, mode=access, exist_ok=False)
            print("Directory ", pathmonth, " Created ")
        except FileExistsError:
            print("Directory ", pathmonth, " already exists")

            return pathyear,pathmonth,today



    def filemanager(self,f):

        md5(f)
        f.save(self.directorymanager()[1] + os.sep + md5.name)






