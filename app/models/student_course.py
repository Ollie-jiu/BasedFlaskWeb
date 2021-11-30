from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Float
from app.models.base import Base

class student_course(Base):
    Index=Column(Integer,primary_key=True,autoincrement=True)
    stuID = Column(Integer, nullable=False)
    courseID=Column(Integer,nullable=False)



    def __init__(self, stuID,courseID,assessmentID,grade):
        super(student_course,self).__init__()
        self.stuID = stuID
        self.courseID=courseID


        
    
    def jsonstr(self):
        jsondata = {
            'stuID':self.stuID,
            'courseID':self.courseID
        }
        return jsondata

    