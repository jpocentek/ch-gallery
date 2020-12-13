from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __str__(self):
        return "{0}: {1}".format(self.__class__.__name__, self.username)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.username)


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False, default="")
    creation_date = Column(DateTime, server_default=func.now())
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship(User, backref=backref('images', uselist=True))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.name)
