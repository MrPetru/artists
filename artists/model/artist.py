# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Boolean
#from sqlalchemy.orm import relation, backref

from artists.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Artist', 'Phone', 'Email', 'Skype', 'Role', 'Tags', 'Software']

artist_role = Table('artist_role', metadata,
    Column('artist_id', Integer, ForeignKey('artist.id')),
    Column('role_id', Integer, ForeignKey('role.id')),
    )
    
artist_software = Table('artist_software', metadata,
    Column('artist_id', Integer, ForeignKey('artist.id')),
    Column('software_id', Integer, ForeignKey('software.id')),
    )

artist_tags = Table('artist_tags', metadata,
    Column('artist_id', Integer, ForeignKey('artist.id')),
    Column('tags_id', Integer, ForeignKey('tags.id')),
    )


class Artist(DeclarativeBase):
    __tablename__ = 'artist'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode, nullable=False)
    lastname = Column(Unicode, nullable=False)
    role = relation('Role', secondary=artist_role, backref='artist')
    software = relation('Software', secondary=artist_software, backref='artist')
    tags = relation('Tags', secondary=artist_tags, backref='artist')
    sitelink = Column(Unicode, nullable=True)
    reellink = Column(Unicode, nullable=True)
    phone = relation('Phone', order_by='Phone.id', backref='artist')
    email = relation('Email', order_by='Email.id', backref='artist')
    skype = relation('Skype', order_by='Skype.id', backref='artist')
    cvlocal = Column(Unicode, nullable=True)
    othercontacts = Column(Unicode, nullable=True)
    newartist = Column(Boolean, nullable=False, default=False)
    note = Column(Unicode, nullable=True)
    address = Column(Unicode, nullable=True)

    # others
    
    #}

class Phone(DeclarativeBase):
    __tablename__ = 'phone'
    #__table_args__ = (UniqueConstraint('artist_id', 'phone'),{})
    id = Column(Integer, primary_key=True)
    phone = Column(Integer, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))  
    #artist = relation(Artist, backref=backref('phone', order_by=id))
    
class Email(DeclarativeBase):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    email = Column(Unicode, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id')) 
#    artist = relation(Artist, backref=backref('email', order_by=id))

class Skype(DeclarativeBase):
    __tablename__ = 'skype'
    id = Column(Integer, primary_key=True)
    skype = Column(Unicode, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id')) 
#    artist = relation(Artist, backref=backref('skype', order_by=id))

class Role(DeclarativeBase):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    #artist = relation(Artist, secondary=artist_role, backref='role')
#    
#    def __init__(self,role):
#        self.name = role
    
class Tags(DeclarativeBase):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    #artist = relation(Artist, secondary=artist_tags, backref='tags')
    
class Software(DeclarativeBase):
    __tablename__ = 'software'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    #artist = relation(Artist, secondary=artist_software, backref='software')
