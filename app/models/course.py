from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import random
from sqlalchemy.sql.sqltypes import DateTime
from app.models.base import Base
import random

class Course(Base):
    # __abstract__ = True # 抽象类 不会生成表
    Index=Column(Integer,primary_key=True,autoincrement=True)
    courseID = Column(Integer,nullable=False)
    name = Column(String(50), nullable=False)
    code=Column(String(20),nullable=False)
    semester=Column(String(50),nullable=False)
    precourseID=Column(Integer,nullable=True,default='0',server_default='0')
    programme=Column(String(50),nullable=False)
    _type=Column('type',String(10),nullable=False)


    def __init__(self, courseID, name, code, semester,precourseID,programme,_type):
        super(Course,self).__init__()
        self.courseID = courseID
        self.name = name
        self.code = code
        self.semester= semester
        self.precourseID=precourseID
        self.programme= programme
        self._type= _type


    
    # def getName(self):
    #     return self.email
    
    # def searchCourse(self,course):
    #     pass
    
    # def searchDegree(self):
    #     pass
    def jsonstr(self):
        jsondata = {
            'courseID' :self.courseID,
            'CourseName':self.name,
            'semester':self.semester,
            'code':self.code,
            'precourseID':self.precourseID,
            'program':self.programme,
            '_type':self._type
        }
        return jsondata
        
    def getprecourseID(self):
        return self.precourseID
    