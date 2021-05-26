from database.models.models import Directories


class DirectoryRepository():

    def getAll(self, user_role):
        self.data = Directories.select().where(Directories.Role == user_role).execute()
        return self.data


    def getOne(self, Id):
        self.data = Directories.select().where(Directories.Id == Id).execute()
        return self.data


    def createOne(self,insert_dict):
        self.data =  Directories.insert(insert_dict).execute()
        return self.data