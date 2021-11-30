from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import user
from app.models.user import User
from app.models.base import db


class Student(User):
    stuID=Column(Integer,unique=True,nullable=False)

    def __init__(self,userID,userName, _password,fullname,programme,stuID):
        super(Student,self).__init__(self, userID,userName, _password,fullname,programme)
        self.stuID=stuID
        

    def jsonstr(self):
        jsondata = {
            'userID': self.userID,
            'userName':self.userName,
            'fullname': self.fullname,
            'programme':self.programme,
            'stuID':self.stuID
        }
        return jsondata