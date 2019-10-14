"""
copyright: 2019 Meisam@wikimedia, MichaelSchoenitzer@wikimedia
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
from datetime import timedelta

logging.basicConfig(filename="telescreen.log", level=logging.DEBUG)

# -----------Slide Sources-----------
# page which lists all the slide-urls
wikipedia_list_page = "Benutzer:Meisam/test"
wikipedia_lang = "de"

# list of the users who are allowed to edit the wikipedia page
whitelist_users = ["Meisam"]

working_directory = "./"

# images will be cached here
cache_folder = ""

# the images included in the wikipedia page will be cached here
# the files in this directory will be completely wiped each time the wikipedia page is updated
wikipedia_list_cache = ""

# the images included in the local list files will be cached here
# directory will be completely wiped each time the slides list is updated
local_lists_cache = ""

# will try to download these types if found in a URL
img_extensions = ("jpeg", "jpg", "png", "gif")
# these types be shown directly
web_extensions = ("htm", "html")
# list files be parsed line-by-line
list_extensions = ("txt",)

# -----------Slide configs-----------
# Update the slides list every ***
cache_lifetime = timedelta(hours=1)


# show each slide for *** seconds
slides_refresh_time = 30
