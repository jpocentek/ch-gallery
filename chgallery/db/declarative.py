from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.username)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.username)
