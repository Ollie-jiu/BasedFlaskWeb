from re import T
from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.schema import Index
from app.models.base import Base

class analysis_course(Base):
    Index=Column(Integer,primary_key=True,autoincrement=True)
    courseID = Column(Integer, nullable=False)
    staffID=Column(Integer, nullable=False)

    def __init__(self,courseID,staffID):
        super(analysis_course,self).__init__(courseID,staffID)
        self.courseID=courseID
        self.staffID=staffID
        
        
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'staffID':self.staffID
        }
        return jsondata

    #sfsgdgdgfggdf
