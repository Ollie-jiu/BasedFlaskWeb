from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.schema import Index
from app.models.base import Base

class Log(Base):
    Index=Column(Integer,primary_key=True,autoincrement=True)
    operation = Column(String(50), nullable=False)
    staffID=Column(Integer, nullable=False)

    def __init__(self,courseID,operation,staffID):
        super(Log,self).__init__(courseID,operation,staffID)
        self.courseID=courseID
        self.operation=operation
        self.staffID=staffID
        
        
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'operation':self.operation,
            'staffID':self.staffID
        }
        return jsondata
