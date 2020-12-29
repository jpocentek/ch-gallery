from flask import url_for
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
        return str(self.username)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.username)


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False, default="")
    creation_date = Column(DateTime, server_default=func.now())
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    author = relationship(User, backref=backref('images', uselist=True))

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.name)

    def url(self):
        """ Returns URL to full sized image file """
        return url_for('image.uploaded_file', filename=self.name)

    def thumbnail_url(self):
        """
        Returns URL of thumbnail image (max size 250px)
        used for main gallery page.
        """
        return url_for('image.uploaded_file_thumbnail', filename=self.name)

    def preview_url(self):
        """
        Returns URL of the smallest picture (max size 100px)
        used as preview on administration pages.
        """
        return url_for('image.uploaded_file_preview', filename=self.name)
