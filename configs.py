"""
copyright: 2019 Meisam@wikimedia
This file is part of Telescreen: A slideshow script for the WikiMUC

    Telescreen is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Telescreen is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Telescreen. If not, see <https://www.gnu.org/licenses/>.
"""
import logging

logging.basicConfig(filename='telescreen.log', level=logging.DEBUG)

# -----------Slide Sources-----------
#page which lists all the slide-urls
wikipedia_list_page = "Benutzer:Meisam/test"
wikipedia_lang = "de"

#list of the users who are allowed to edit the wikipedia page
whitelist_users = ["Meisam"]

working_directory = "./"

#the files in this directory will be completely wiped each time the wikipedia page is updated
wikipedia_cache = ""

#content of the wikipedia page will be kept here
wikipedia_listfile = ""

#the files in this directory will be completely wiped each time the slides list is
lists_cache = ""

#will try to download these types if found in a URL
extensions_img = ('jpeg', 'jpg', 'png', 'gif')
#these types be shown directly
extensions_web = ('htm', 'html')
#list files be parsed line-by-line
extensions_list = ('txt',)

# -----------Slide configs-----------
#Update the slides list every *** seconds
cache_lifetime = 1 * 3600

#show each slide for *** seconds
slides_refresh_time = 30
