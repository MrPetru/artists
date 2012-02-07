# -*- coding: utf-8 -*-
"""Setup the artists application"""

import logging
from tg import config
from artists import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup artists here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'admin'
        u.display_name = u'Local Admin'
        u.email_address = u'admin@localhost.com'
        u.password = u'none'
    
        model.DBSession.add(u)
    
        g = model.Group()
        g.group_name = u'admins'
        g.display_name = u'Admins Group'
    
        g.users.append(u)
    
        model.DBSession.add(g)
    
        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right'
        p.groups.append(g)
    
        model.DBSession.add(p)
    
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>
