from sqlalchemy import Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.sql.sqltypes import DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    firstname = Column(String(25), nullable=False)
    lastname = Column(String(25), nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, index=True)
    birthday = Column(DateTime, default=None)
    description = Column(String(150), default='')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
