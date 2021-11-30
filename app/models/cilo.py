from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class CILO(Base):
    ciloID=Column(Integer,nullable=False,primary_key=True,unique=True)
    name = Column(String(50), nullable=False)
    description=Column(String(100), nullable=True)

    def __init__(self,ciloID,name,description):
        super(CILO,self).__init__(ciloID,name,description)
        self.ciloID=ciloID
        self.name=name
        self.description = description
        
    
    def jsonstr(self):
        jsondata = {
            'ciloID':self.ciloID,
            'name':self.name,
            'description':self.description

        }
        return jsondata

    #sfsgdgdgfggdf
