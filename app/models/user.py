from sqlalchemy import Column, String, Integer, orm
from app.models.base import Base

class User(Base):
    __abstract__ = True # 抽象类 不会生成表
    
    userID = Column(Integer,unique=True,primary_key=True)
    userName = Column(String(50), unique=True, nullable=False)#user email
    _password = Column('password', String(100),nullable=False,default='123456',server_default='123456')
    fullname = Column(String(50), nullable=False)
    programme= Column(String(50), nullable=False)

    def __init__(self, userID,userName, _password,fullname,programme):
        super(User,self).__init__()
        self.userID = userID
        self.userName = userName
        self._password = _password
        self.fullname = fullname
        self.programme=programme
    
    def getuserName(self):
        return self.userName

    