# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
"""BibFormat element - Prints physical description of the item
"""

import cgi
import re

def format_element(bfo, prefix_en="", prefix_es="",
                   prefix_fr=""):


    pages = bfo.field('5050_a')

    if len(pages) == 0:
        pages = bfo.field('5051_a')

    if len(pages) == 0:
        pages = bfo.field('5052_a')

    #pages = re.sub(':$', '', pages)
    out = '''
        %s 
    ''' % pages
     
    if len(pages) > 0:
        if bfo.lang == 'es':
            prefix = prefix_es
        elif bfo.lang == 'fr':
            prefix = prefix_fr
        else:
            prefix = prefix_en        
        return prefix + out


def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0

