## -*- coding: utf-8 -*-
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
"""BibFormat element - Prints authors
"""
__revision__ = "$Id$"


def format_element(bfo, limit, prefix_en="", prefix_es="",
                   prefix_fr="", separator=' ; ',
                   extension='[...]',
                   print_links="yes",
                   print_affiliations='no',
                   affiliation_prefix = ' (',
                   affiliation_suffix = ')',
                   interactive="no",
                   highlight="no"):
    """
    Prints the list of authors of a record.

    @param limit: the maximum number of authors to display
    @param separator: the separator between authors.
    @param extension: a text printed if more authors than 'limit' exist
    @param print_links: if yes, prints the authors as HTML link to their publications
    @param print_affiliations: if yes, make each author name followed by its affiliation
    @param affiliation_prefix: prefix printed before each affiliation
    @param affiliation_suffix: suffix printed after each affiliation
    @param interactive: if yes, enable user to show/hide authors when there are too many (html + javascript)
    @param highlight: highlights authors corresponding to search query if set to 'yes'
    """
    from urllib import quote
    from cgi import escape
    from invenio.config import CFG_SITE_URL
    from invenio.messages import gettext_set_language
    import re

    authors = []
    authors_1 = bfo.fields('1001_')
    authors_2 = bfo.fields('7001_')
    authors_3 = bfo.fields('1101_')
    authors_4 = bfo.fields('1102_')
    authors_5 = bfo.fields('7102_')
    authors_6 = bfo.fields('7101_')

    # VS check if ILO convention

    conv = bfo.field('970__a')

    # VS hack to take away links from corporate authors

    if authors_3:
        if print_links.lower() == "yes":
            for item in authors_3:
                if item.has_key('a'):
                    itema = str(item.get("a", " "))
                    itema = 'CORP' + itema
                    item.update({'a': itema})
    if authors_4:
        if print_links.lower() == "yes":
            for item in authors_4:
                if item.has_key('a'):
                    itema = str(item.get("a", " "))
                    itema = 'CORP' + itema
                    item.update({'a': itema})

    # VS hack not to print author in ILO conventions

    if authors_5 and conv.startswith('ILOCONV'):
        if print_links.lower() == "yes":
            for item in authors_5:
                if item.has_key('a'):
                    itema = str(item.get("a", " "))
                    itema = ''
                    #item.update({'a': itema})
                    item.clear()

    authors.extend(authors_1)
    authors.extend(authors_2)
    authors.extend(authors_3)
    authors.extend(authors_4)
    authors.extend(authors_5)
    authors.extend(authors_6)

    nb_authors = len(authors)

    if nb_authors:
        if bfo.lang == 'es':
            prefix = prefix_es
        elif bfo.lang == 'fr':
            prefix = prefix_fr
        else:
            prefix = prefix_en

        # Process authors to add link, highlight and format affiliation
        for author in authors:

            if author.has_key('a'):
                if highlight == 'yes':
                    from invenio import bibformat_utils
                    author['a'] = bibformat_utils.highlight(author['a'],
                                                            bfo.search_pattern)

                # VS hack to take away links from corporate authors
                if print_links.lower() == "yes":
                    if author['a'].startswith('CORP'):
                        author['a'] = re.sub('^CORP', '', author['a'])
                    else:
                        #author['a'] = '<a  class="detailsAuthors" href="' + CFG_SITE_URL + \
                        #              '/search?f=author&amp;p='+ quote(author['a']) + \
                        #              '&amp;ln='+ bfo.lang + \
                        #              '">'+escape(author['a'])+'</a>'
                        author['a'] = '<a  class="detailsAuthors" href="' + CFG_SITE_URL + \
                                      '/search?f=author&amp;p='+ quote(author['a']) + \
                                      '&amp;ln='+ bfo.lang + \
                                      '">'+(author['a'])+'</a>'

            if author.has_key('u'):
                if print_affiliations == "yes":
                    author['u'] = affiliation_prefix + author['u'] + \
                                  affiliation_suffix

            if author.has_key('b'):
                if print_affiliations == "yes":
                    author['b'] = affiliation_prefix + author['b'] + \
                                  affiliation_suffix

        # Flatten author instances
        if print_affiliations == 'yes':
            authors = [author.get('a', '') + author.get('u', '') + author.get('b', '')
                       for author in authors]
        else:
            authors = [author.get('a', '') + author.get('b', '')
                       for author in authors]

        if limit.isdigit() and  nb_authors > int(limit) and interactive != "yes":
            out = separator.join(authors[:int(limit)]) + extension

        elif limit.isdigit() and nb_authors > int(limit) and interactive == "yes":
            out = '''
            <script type="text/javascript">
            function toggle_authors_visibility(){
                var more = document.getElementById('more');
                var link = document.getElementById('link');
                var extension = document.getElementById('extension');
                if (more.style.display=='none'){
                    more.style.display = '';
                    extension.style.display = 'none';
                    link.innerHTML = "%(show_less)s"
                } else {
                    more.style.display = 'none';
                    extension.style.display = '';
                    link.innerHTML = "%(show_more)s"
                }
                link.style.color = "rgb(204,0,0);"
            }

            function set_up(){
                var extension = document.getElementById('extension');
                extension.innerHTML = "%(extension)s";
                toggle_authors_visibility();
            }

            </script>
            '''%{'show_less':_("Hide"),
                 'show_more':_("Show all %i authors") % nb_authors,
                 'extension':extension}

            out += '<a name="show_hide" />'
            out += separator.join(authors[:int(limit)])
            out += '<span id="more" style="">' + separator + \
                   separator.join(authors[int(limit):]) + '</span>'
            out += ' <span id="extension"></span>'
            out += ' <small><i><a class="detailsAuthors" id="link" href="#" onclick="toggle_authors_visibility()" style="color:rgb(204,0,0);"></a></i></small>'
            out += '<script type="text/javascript">set_up()</script>'
        elif nb_authors > 0:
            out = separator.join(authors)

        return prefix + out

def escape_values(bfo):
    """
    Called by BibFormat in order to check if output of this element
    should be escaped.
    """
    return 0