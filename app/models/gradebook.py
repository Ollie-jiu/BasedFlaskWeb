from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Float
from app.models.base import Base

class Gradebook(Base):
    Index=Column(Integer,primary_key=True,autoincrement=True)
    courseID=Column(Integer,nullable=False)
    stuID=Column(Integer,nullable=False)
    semester=Column(String(20),nullable=False)
    # CILO=Column(String(20),nullable=False)
    Assessment_type=Column(String(30),nullable=False)
    mark=Column(Float,nullable=False)
    
    def __init__(self,courseID,stuID,semester,Assessment_type,mark):
        super(Gradebook,self).__init__(courseID,stuID,semester,Assessment_type,mark)
        self.courseID=courseID
        self.stuID=stuID
        self.semester=semester
        # self.CILO=CILO
        self.Assessment_type=Assessment_type
        self.mark=mark
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'stuID':self.stuID,
            'semester':self.semester,
            'Assessment_type':self.Assessment_type,
            'mark':self.mark
        }
        return jsondata