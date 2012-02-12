# -*- coding: utf-8 -*-

import tw2.core as twc, tw2.forms as twf
from tg import redirect, config, url
from tw.forms.validators import Int, NotEmpty, DateConverter, Email, String
import formencode
from formencode import schema

class FileInput(twf.FileField):
    size = twc.Param('Custom CSS class', default='', attribute=True)
    
class AddForm(twf.TableForm):
    action = '/artist/post_add'
    css_class = "add_new_artist"
    firstname = twf.TextField(label='Nome:', validator=NotEmpty)
    lastname = twf.TextField(label='Cognome:', validator=NotEmpty)
    role = twf.TextField(label='Ruolo:', validator=NotEmpty)
    software = twf.TextField(label='Software:', validator=NotEmpty)
    tags = twf.TextField(label='Tags:', validator=NotEmpty)
    phone = twf.TextField(label='Phone:')
    email = twf.TextField(label='Email:')
    skype = twf.TextField(label='Skype:')
    cv_upload = FileInput(label='CV Uplod:', size='43')
    note = twf.TextArea(label='Description:')
    sitelink = twf.TextField(label='Site Links:')
    reellink = twf.TextField(label='Reel Links')
    othercontacts = twf.TextField(label='Other Info:')
    newartist = twf.RadioButtonList(label='New Artist:', options=[(1, 'YES'),(0, 'NO')], default=1)
    
class Container(twc.Widget):
    template = 'mako:artists.templates.widgets_templates.container'
    css_class = twc.Param('Custom CSS class', default='')
    text = twc.Param('A simple text value', default='')
    
class ArtistInfo(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_info'
    name = Container(css_class = "artist_info_line")
    role = Container(css_class = "artist_info_line")
    software = Container(css_class = "artist_info_line")
    tags = Container(css_class = "artist_info_line")
    
class ArtistLink(Container):
    template = 'mako:artists.templates.widgets_templates.artist_link'
        
class ArtistLinks(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_links'
    void = Container(css_class = "artist_link", text='')
    sitelink = ArtistLink(css_class = "artist_link", text='SITE')
    cv = ArtistLink(css_class = "artist_link", text='CV')
    contacts = ArtistLink(css_class = "artist_link", text='CONTACTS')

class ArtistShortDescription(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_short_description'
    artist_title = Container(css_class = "artist_title")
    artist_short_description = Container(css_class = "artist_description")

class ArtistUpdateButton(Container):
    template = 'mako:artists.templates.widgets_templates.artist_update_button'
    text = 'AGGIORNA'
    
class ArtistSystem(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_system'
    text = 'aggiornato il:'
    lastupdate = Container(css_class = "artist_last_update")
    artist_to_update = ArtistUpdateButton(css_class='artist_update_button')

class ArtistRow(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_row'
    photo = Container(css_class = "artist_photo")
    separator_void = Container(css_class = "separator_void")
    artist_info = ArtistInfo(css_class = "artist_info")
    separator_line_1_h = Container(css_class = "separator_line")
    artist_links = ArtistLinks(css_class = "artist_links")
    separator_line_2_h = Container(css_class = "separator_line")
    artist_description = ArtistShortDescription(css_class = "artist_short_description")
    eparator_line_3_h = Container(css_class = "separator_line")
    artist_system = ArtistSystem(css_class = "artist_system")
    
class AristTable(twc.RepeatingWidget):
    template = 'mako:artists.templates.widgets_templates.artist_table'
    child = ArtistRow
    
    
    
