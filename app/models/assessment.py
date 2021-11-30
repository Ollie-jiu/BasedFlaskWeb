from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import Float
from app.models.base import Base,db


class assessment(Base):
    Index=Column(Integer,primary_key=True,autoincrement=True)
    courseID=Column(Integer,nullable=False)
    Semester=Column(String(20),nullable=False)
    CILO=Column(String(20),nullable=False)
    _type=Column('type',String(30),nullable=False)
    weight=Column(Float,nullable=False)
    
    def __init__(self,courseID,Semester,CILO,_type,weight):
        super(assessment,self).__init__()
        self.courseID=courseID
        self.Semester=Semester
        self.CILO=CILO
        self._type=_type
        self.weight=weight
    
    def jsonstr(self):
        jsondata = {
            'courseID':self.courseID,
            'Semester':self.Semester,
            'CILO':self.CILO,
            '_type':self._type,
            'weight':self.weight
        }
        return jsondata