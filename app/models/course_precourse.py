from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class course_precourse(Base):
    number=Column(Integer,primary_key=True)
    courseID=Column(Integer,nullable=False)
    precourseID=Column(Integer,nullable=False)
    ciloName=Column(String(20),nullable=False)
    
    def __init__(self,courseID,precourseID,ciloName):
        super(course_precourse,self).__init__()
        self.courseID=courseID
        self.precourseID=precourseID
        self.ciloName=ciloName
        
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'precourseID':self.precourseID,
            'ciloName':self.ciloName
        }
        return jsondata