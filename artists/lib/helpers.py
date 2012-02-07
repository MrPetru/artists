# -*- coding: utf-8 -*-

"""WebHelpers used in artists."""

from webhelpers import date, feedgenerator, html, number, misc, text

def get_list_from_string(text):
    """
    return a list from a string, keywords separated from simbol(,)
    """
    tmp = text
    if len(tmp)<1:
        return ''
    if tmp[0] != ',':
        tmp = ',' + tmp
    
    while -1 < tmp.find('  '):
        tmp = tmp.replace('  ', ' ')
    
    while -1 < tmp.find(', '):
        tmp = tmp.replace(', ', ',')
    
    while -1 < tmp.find(' ,'):
        tmp = tmp.replace(' ,', ',')
    
    tmp2 = []
    for element in tmp.split(','):
        if element != '':
            tmp2.append(element)
            
    return tmp2
