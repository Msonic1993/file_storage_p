from peewee import IntegerField, CharField, DecimalField, DateField
from database.database import BaseModel


class Directories(BaseModel):
    __tablename__ = "directories"
    Id = IntegerField(null=False, unique=True)
    Name = CharField(null=False)
    Role = CharField(null=True)


class Files(BaseModel):
    __tablename__ = "files"
    id = IntegerField(null=False)
    name = CharField(null=False)
    path = CharField(null=True)
    filesize = DecimalField(null=True)
    creationdate = DateField(null=True)
    directoryId = IntegerField(null=False)
    username = CharField(null=True)