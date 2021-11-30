from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class course_cilo(Base):
    number=Column(Integer,primary_key=True)
    courseID=Column(Integer,nullable=False)
    ciloName=Column(String(20),nullable=False)
    description=Column(String(100),nullable=False)
    
    def __init__(self,courseID,ciloName,description):
        super(course_cilo,self).__init__()
        self.courseID=courseID
        self.ciloName=ciloName
        self.description=description
        
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'ciloName':self.ciloName,
            'description':self.description
        }
        return jsondata