# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose, require, validate
from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from artists.lib.base import BaseController
#from artists.model import DBSession, metadata
from artists.model import *
from artists.model.artist import * #Artist, Role
from repoze.what import predicates
from tg import redirect, config, url, tmpl_context, response
#from artists.model import DeclarativeBase, metadata, DBSession

from repoze.what.predicates import in_group
import tw2.core, tw2.forms
import transaction
from artists.lib import helpers
import formencode
from formencode import schema

import shutil, mimetypes, pylons
from datetime import datetime

from artists.lib.widgets import AristTable, AddForm


#add_form = AddForm()
get_all_form = AristTable()
add_form = AddForm()

class GetAllTble(tw2.forms.TableLayout):
    pass

class Controller(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose()
    def default(self):
        redirect('/artist/get_all')
    
    @expose()    
    def contacts(self):
        return ("<h1>PAGE NOT FOUND</h1>")
    
    @require(in_group('admins'))   
    @expose('artists.templates.get_all')
    def get_all(self):
        artists = DBSession.query(Artist).order_by(Artist.firstname).all()
        tmpl_context.get_all_form = get_all_form
        return dict(page='artists', artists=artists)
    
    @require(in_group('admins')) 
    @expose('artists.templates.add_page')
    def add(self, **kwargs):
        
        if isinstance(kwargs, dict):
            kwargs['error'] = pylons.tmpl_context.form_errors
            arguments = kwargs
        w = add_form(value = arguments)
        return dict(widget=w, page='add page')
    
    @require(in_group('admins')) 
    @expose('artists.templates.add_page')    
    def edit(self, firstname, lastname):
        artist = DBSession.query(Artist).filter_by(firstname=firstname, lastname=lastname).all()
        data = artist[0].__dict__
        role = ''
        for i in artist[0].role: role += i.name + ', '
        data['role'] = role
        software = ''
        for i in artist[0].software: software += i.name + ', '
        data['software'] = software
        tags = ''
        for i in artist[0].tags: tags += i.name + ', '
        data['tags'] = tags
        phone = ''
        for i in artist[0].phone: phone += str(i.name) + ', '
        data['phone'] = phone
        email =''
        for i in artist[0].email: email += i.name + ', '
        data['email'] = email
        skype =''
        for i in artist[0].skype: skype += i.name + ', '
        data['skype'] = skype
        reellink =''
        for i in artist[0].reellink: reellink += i.name + ', '
        data['reellink'] = reellink
        
        w = add_form(value = data, action = "/artist/update")
        return dict(widget=w, page='edit artist')
        
    @expose()
    @validate(add_form, error_handler=edit)
    def update(self, firstname='', lastname='', sitelink='', reellink='',
                    role='', software='', tags='', phone='', email='', skype='', othercontacts='',
                    note='', newartist='', cv_upload='', vote=0):
        artist = DBSession.query(Artist).filter_by(firstname=firstname, lastname=lastname).all()[0]
        
        artist.firstname=firstname
        artist.lastname=lastname
        artist.sitelink=sitelink
        artist.note = note
        artist.newartist = newartist
        artist.othercontacts = othercontacts
        artist.last_update = datetime.now()
        artist.rate=0
        
        if hasattr(cv_upload, 'filename'):
            ext = shutil.os.path.splitext(cv_upload.filename)[1]
            dest_path = config['cv_repo']
            dest_path = shutil.os.path.join(dest_path,"%s_%s%s" % (firstname, lastname, ext))
            f = open(dest_path, 'wb')
            f.write(cv_upload.file.read())
            f.close()
            artist.cvlocal = ("%s_%s%s" % (firstname, lastname, ext))
        
        def update_column(info, artist, query, table):
            data_list = helpers.get_list_from_string(info)
            artist_role_list =[]
            for_remove = []
            
            for r in artist:
                if r.name in data_list:
                    artist_role_list.append(r.name)
                else:
                    for_remove.append(r)
            for r in for_remove:
                artist.remove(r)
            for r in data_list:
                if r not in artist_role_list:
                    query_result = query.filter_by(name=r).all()
                    if len(query_result) <= 0:
                        query_result = table(name=r)
                    else:
                        query_result = query.filter_by(name=r).one()
                    artist.append(query_result)
        
        update_column(role, artist.role, DBSession.query(Role), Role)
        update_column(software, artist.software, DBSession.query(Software), Software)
        update_column(reellink, artist.reellink, DBSession.query(Reellink), Reellink)
        update_column(tags, artist.tags, DBSession.query(Tags), Tags)
        update_column(phone, artist.phone, DBSession.query(Phone), Phone)
        update_column(email, artist.email, DBSession.query(Email), Email)
        update_column(skype, artist.skype, DBSession.query(Skype), Skype)
        
            
##        data_list = helpers.get_list_from_string(role)
##        artist_role_list =[]
##        for_remove = []
##        for r in artist.role:
##            if r.name in data_list:
##                artist_role_list.append(r.name)
##            else:
##                for_remove.append(r)
##        for r in for_remove:
##            artist.role.remove(r)
##            
##        for r in data_list:
##            if r not in artist_role_list:
##                query_result = DBSession.query(Role).filter_by(name=r).all()
##                if len(query_result) == 0:
##                    query_result = Role(name=r)
##                else:
##                    query_result = DBSession.query(Role).filter_by(name=r).one()
##                artist.role.append(query_result)
        
        DBSession.add(artist)        
        transaction.commit()
        redirect('/artist/get_all')    
        
       
    
    @expose()
    @validate(add_form, error_handler=add)
    def post_add(self, firstname='', lastname='', sitelink='', reellink='',
                    role='', software='', tags='', phone='', email='', skype='', othercontacts='',
                    note='', newartist='', cv_upload='', vote=0):
                    
        artist = DBSession.query(Artist).filter_by(firstname=firstname, lastname=lastname).all()
        if len (artist) > 0:
            redirect('/artist/get_all')
        
        artist = Artist(firstname=firstname, lastname=lastname, sitelink=sitelink, 
                    note = note, newartist = newartist, othercontacts = othercontacts,
                    last_update = datetime.now(), rate=0)
        
        if hasattr(cv_upload, 'filename'): #== 'instance': # != ('' or None):
            ext = shutil.os.path.splitext(cv_upload.filename)[1]
            dest_path = config['cv_repo']
            dest_path = shutil.os.path.join(dest_path,"%s_%s%s" % (firstname, lastname, ext))
            f = open(dest_path, 'wb')
            f.write(cv_upload.file.read())
            f.close()
            artist.cvlocal = ("%s_%s%s" % (firstname, lastname, ext))
        
        data_list = helpers.get_list_from_string(role)
        for d in data_list:
            query_result = DBSession.query(Role).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Role(name=d)
            else:
                query_result = DBSession.query(Role).filter_by(name=d).one()
                
            artist.role.append(query_result)
        
        data_list = helpers.get_list_from_string(software)
        for d in data_list:
            query_result = DBSession.query(Software).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Software(name=d)
            else:
                query_result = DBSession.query(Software).filter_by(name=d).one()
                
            artist.software.append(query_result)
        
        data_list = helpers.get_list_from_string(tags)
        for d in data_list:
            query_result = DBSession.query(Tags).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Tags(name=d)
            else:
                query_result = DBSession.query(Tags).filter_by(name=d).one()
                
            artist.tags.append(query_result)
            
        data_list = helpers.get_list_from_string(reellink)
        for d in data_list:
            query_result = DBSession.query(Reellink).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Reellink(name=d)
            else:
                query_result = DBSession.query(Reellink).filter_by(name=d).one()
                
            artist.reellink.append(query_result)
        
        data_list = helpers.get_list_from_string(phone)   
        for d in data_list:
            query_result = DBSession.query(Phone).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Phone(name=d)
            else:
                query_result = DBSession.query(Phone).filter_by(name=d).one()
                
            artist.phone.append(query_result)
        
        data_list = helpers.get_list_from_string(email)   
        for d in data_list:
            query_result = DBSession.query(Email).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Email(name=d)
            else:
                query_result = DBSession.query(Email).filter_by(name=d).one()
                
            artist.email.append(query_result)
            
        data_list = helpers.get_list_from_string(skype)   
        for d in data_list:
            query_result = DBSession.query(Skype).filter_by(name=d).all()
            if len(query_result) == 0:
                query_result = Skype(name=d)
            else:
                query_result = DBSession.query(Skype).filter_by(name=d).one()
                
            artist.skype.append(query_result)
            
        DBSession.add(artist)        
        transaction.commit()
        redirect('/artist/get_all')
        
    @expose()
    def download(self, file_name):
        firstname, lastname = file_name.split('_')
        artist = DBSession.query(Artist).filter_by(firstname=firstname, lastname=lastname).all()
        cvlocal = artist[0].cvlocal
        path = shutil.os.path.join(config['cv_repo'], cvlocal)
        f = open(path)
        
        # set the correct content-type so the browser will know what to do
        content_type, encoding = mimetypes.guess_type(path)
        response.headers['Content-Type'] = content_type
        response.headers['Content-Disposition'] = (
                                        ('attachment; filename=%s' %
                                            file_name).encode())
        
        # copy file content in the response body
        shutil.copyfileobj(f, response.body_file)
        f.close()
        return
