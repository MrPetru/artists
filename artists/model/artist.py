# -*- coding: utf-8 -*-
"""Sample model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Boolean, DateTime
from tg import url
from datetime import datetime
#from sqlalchemy.orm import relation, backref

from artists.model import DeclarativeBase, metadata, DBSession

__all__ = [ 'Artist', 'Phone', 'Email', 'Skype', 'Role', 'Tags', 'Software', 'Reellink']

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
    reellink = relation('Reellink', order_by='Reellink.id', backref='artist')
    phone = relation('Phone', order_by='Phone.id', backref='artist')
    email = relation('Email', order_by='Email.id', backref='artist')
    skype = relation('Skype', order_by='Skype.id', backref='artist')
    cvlocal = Column(Unicode, nullable=True)
    presentation = Column(Unicode, nullable=True)
    othercontacts = Column(Unicode, nullable=True)
    newartist = Column(Boolean, nullable=False, default=False)
    note = Column(Unicode, nullable=True)
    address = Column(Unicode, nullable=True)
    last_update = Column(DateTime, default=datetime.now())
    rate = Column(Integer, default=0, nullable=False)

    # others
    
    #}
    
    @property
    def artist_info(self):
        name = '%s %s' % (self.firstname, self.lastname)
        role = ''
        for r in self.role:
            role += r.name + ', '
        software = ''
        for s in self.software:
            software += s.name + ', '
        tags = ''
        for t in self.tags:
            tags += t.name + ', '
        return {'name': name, 'role': role, 'software':software, 'tags':tags}
        
    @property
    def artist_links(self):
        if self.cvlocal:
            cv = url('download/' + self.cvlocal)
        else: cv = None
        
        
        if (len(self.sitelink) > 0) and (not self.sitelink[0:7] == 'http://'):
            sitelink = 'http://' + self.sitelink
        elif (len(self.sitelink) > 0) and (self.sitelink[0:7] == 'http://'):
            sitelink = self.sitelink
        else:
            sitelink = None
            
        return {'sitelink': sitelink, 'cv':cv, 'contacts':'contacts'}
        
    @property
    def artist_description(self):
        return {'artist_short_description':'&nbsp;&nbsp;&nbsp;&nbsp;%s' % self.note,
        'artist_title' : "Short description:"}
        
    @property
    def artist_system(self):
        lastupdate = str(self.last_update)[:19]
        artist_to_update = "edit/%s/%s" % (self.firstname, self.lastname)
        return {'lastupdate':lastupdate, 'artist_to_update':url(artist_to_update), 'rate':str(self.rate)}

class Phone(DeclarativeBase):
    __tablename__ = 'phone'
    #__table_args__ = (UniqueConstraint('artist_id', 'phone'),{})
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))  
    #artist = relation(Artist, backref=backref('phone', order_by=id))
    
class Reellink(DeclarativeBase):
    __tablename__ = 'reellink'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id'))  
    
class Email(DeclarativeBase):
    __tablename__ = 'email'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
    artist_id = Column(Integer, ForeignKey('artist.id')) 
#    artist = relation(Artist, backref=backref('email', order_by=id))

class Skype(DeclarativeBase):
    __tablename__ = 'skype'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, unique=True)
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
