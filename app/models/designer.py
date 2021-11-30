from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from app.models.lecturer import Lecturer
from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.functions import user
from app.models.user import User


class Designer(User):
    staffID=Column(Integer,nullable=False)

    def __init__(self,userID,userName, _password,fullname,programme,staffID):
        super(Designer,self).__init__(self, userID,userName, _password,fullname,programme)
        self.staffID=staffID
        

    def jsonstr(self):
        jsondata = {
            'userID': self.userID,
            'userName':self.userName,
            'fullname': self.fullname,
            'programme':self.programme,
            'staffID':self.staffID
        }
        return jsondata