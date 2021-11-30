from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import user
from app.models.user import User


class Lecturer(User):
    staffID=Column(Integer,nullable=False)

    def __init__(self,userID,userName, _password,fullname,programme,staffID):
        super(Lecturer,self).__init__(self, userID,userName, _password,fullname,programme)
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