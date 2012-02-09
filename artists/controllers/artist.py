# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose, require, validate
#from tg import redirect, validate, flash

# third party imports
#from tg.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from artists.lib.base import BaseController
#from artists.model import DBSession, metadata
from artists.model import *
from artists.model.artist import * #Artist, Role
from repoze.what import predicates
from tg import redirect, config, url
#from artists.model import DeclarativeBase, metadata, DBSession

from repoze.what.predicates import in_group
import tw2.core, tw2.forms
import transaction
from artists.lib import helpers

import shutil

class AddForm(tw2.forms.TableForm):
            action = '/artist/post_add'
            firstname = tw2.forms.TextField(label='NOME', validator=tw2.core.Required)
            lastname = tw2.forms.TextField(label='COGNOME', validator=tw2.core.Required)
            sitelink = tw2.forms.TextField(label='SITE LINK', validator=tw2.core.Required)
            reellink = tw2.forms.TextField(label='REEL LINK', validator=tw2.core.Required)
            role = tw2.forms.TextField(label='RUOLO', validator=tw2.core.Required)
            software = tw2.forms.TextField(label='SOFTWARE', validator=tw2.core.Required)
            tags = tw2.forms.TextField(label='TAGS', validator=tw2.core.Required)
            phone = tw2.forms.TextField(label='PHONE', validator=tw2.core.Required)
            email = tw2.forms.TextField(label='EMAIL', validator=tw2.core.Required)
            skype = tw2.forms.TextField(label='SKYPE', validator=tw2.core.Required)
            othercontacts = tw2.forms.TextField(label='OTHER CONTACTS', validator=tw2.core.Required)
            note = tw2.forms.TextArea(label='NOTE', validator=tw2.core.Required)
            cv_upload = tw2.forms.FileField()
            newartist = tw2.forms.RadioButtonList(label='NEW ARTIST', options=[[1, 'YES'],[0, 'NO']], default=1)
            
#add_form = AddForm(redirect='/artis/get_all').req()
add_form = AddForm()

class GetAllTble(tw2.forms.TableLayout):
    pass

class Controller(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose()
    def default(self):
        redirect('/artist/get_all')
    
    @require(in_group('admins'))   
    @expose('artists.templates.get_all')
    def get_all(self):
        artists = DBSession.query(Artist).order_by(Artist.firstname).all()
        return dict(page='artists', artists=artists)
    
    @require(in_group('admins')) 
    @expose('artists.templates.add_page')
    def add(self, **kwargs):
        
        w = AddForm(redirect='/artis/get_all').req()
        return dict(widget=w, page='add page')
    
    @expose()
    @validate(add_form, error_handler=add)
    def post_add(self, firstname='', lastname='', sitelink='', reellink='',
                    role='', software='', tags='', phone='', email='', skype='', othercontacts='',
                    note='', newartist='', cv_upload=''):
        print (firstname, lastname, sitelink, reellink, role, software, tags, phone, email, skype,
                othercontacts, note, newartist)
        
        artist = Artist(firstname=firstname, lastname=lastname, sitelink=sitelink, reellink=reellink, 
                    note = note, newartist = newartist, othercontacts = othercontacts)
        
        if cv_upload != '':
            ext = shutil.os.path.splitext(cv_upload.filename)[1]
            dest_path = config['cv_repo']
            dest_path = shutil.os.path.join(dest_path,"%s_%s%s" % (firstname, lastname, ext))
            f = open(dest_path, 'wb')
            f.write(cv_upload.file.read())
            f.close()
            artist.cvlocal = ("%s_%s%s" % (firstname, lastname, ext))
            print (url(artist.cvlocal))
            print (url('/ds'))
        
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
        
        data_list = helpers.get_list_from_string(phone)   
        for d in data_list:
            query_result = DBSession.query(Phone).filter_by(phone=d).all()
            if len(query_result) == 0:
                query_result = Phone(phone=d)
            else:
                query_result = DBSession.query(Phone).filter_by(phone=d).one()
                
            artist.phone.append(query_result)
        
        data_list = helpers.get_list_from_string(email)   
        for d in data_list:
            query_result = DBSession.query(Email).filter_by(email=d).all()
            if len(query_result) == 0:
                query_result = Email(email=d)
            else:
                query_result = DBSession.query(Email).filter_by(email=d).one()
                
            artist.email.append(query_result)
            
        data_list = helpers.get_list_from_string(skype)   
        for d in data_list:
            query_result = DBSession.query(Skype).filter_by(skype=d).all()
            if len(query_result) == 0:
                query_result = Skype(skype=d)
            else:
                query_result = DBSession.query(Skype).filter_by(skype=d).one()
                
            artist.skype.append(query_result)
            
        DBSession.add(artist)        
        transaction.commit()
        redirect('/artist/get_all')
        
    @expose()
    def download(self, file_name):
    
        f = shutil.os.path.join(config['cv_repo'], file_name)
        
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
