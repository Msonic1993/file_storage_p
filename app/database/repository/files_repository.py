from database.models.models import Directories, Files


class FilesRepository:

    def getAll(self, Id):
        self.data = Files.select().join(Directories, on=(Directories.id == Files.directoryId)).where( Directories.Id == Id)
        return self.data

    def getOne(self, Id):
        self.data = Files.select().where(Files.id == Id).limit(1)
        return self.data



    def createOne(self,insert_dict):
        self.data = Files.insert(insert_dict).execute()
        return self.data



    def clearOne(self, Id):
        self.data = Files.delete().where(Files.id == Id).execute()
        return self.data
