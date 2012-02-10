# -*- coding: utf-8 -*-

import tw2.core as twc, tw2.forms as twf
from tg import redirect, config, url

class AddForm(twf.TableForm):
    action = '/artist/post_add'
    firstname = twf.TextField(label='NOME', validator=twc.Required)
    lastname = twf.TextField(label='COGNOME', validator=twc.Required)
    sitelink = twf.TextField(label='SITE LINK', validator=twc.Required)
    reellink = twf.TextField(label='REEL LINK', validator=twc.Required)
    role = twf.TextField(label='RUOLO', validator=twc.Required)
    software = twf.TextField(label='SOFTWARE', validator=twc.Required)
    tags = twf.TextField(label='TAGS', validator=twc.Required)
    phone = twf.TextField(label='PHONE', validator=twc.Required)
    email = twf.TextField(label='EMAIL', validator=twc.Required)
    skype = twf.TextField(label='SKYPE', validator=twc.Required)
    othercontacts = twf.TextField(label='OTHER CONTACTS', validator=twc.Required)
    note = twf.TextArea(label='NOTE', validator=twc.Required)
    cv_upload = twf.FileField()
    newartist = twf.RadioButtonList(label='NEW ARTIST', options=[[1, 'YES'],[0, 'NO']], default=1)
    

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
    reel = ArtistLink(css_class = "artist_link", text='REEL')
    cv = ArtistLink(css_class = "artist_link", text='CV')
    contacts = ArtistLink(css_class = "artist_link", text='CONTACTS')

class ArtistShortDescription(twc.CompoundWidget):
    template = 'mako:artists.templates.widgets_templates.artist_short_description'
    artist_title = Container(css_class = "artist_title")
    artist_short_description = Container(css_class = "artist_description")

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
    artist_system = Container(css_class = "artist_system")
    
class AristTable(twc.RepeatingWidget):
    template = 'mako:artists.templates.widgets_templates.artist_table'
    child = ArtistRow
    
    
    
