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

## -----------Auto-Update-----------
##automatically update the Telescreen from the master branch in the git repo
#script_auto_update = True
#
##check for the new version of this script every *** seconds!
#script_lifetime = 24 * 3600

# -----------Slide Sources-----------
#page which lists all the slide-urls
wikipedia_list_page = "Benutzer:Meisam/test"
wikipedia_lang = "de"

#list of the users who are allowed to edit the wikipedia page
whitelist_users = ["Meisam"]

working_directory = "./"

#the files in this directory will be completely wiped each time the slide list is updated
downloads_directory = working_directory + "/cache"

# -----------Slide configs-----------
#Update the slides list every *** seconds
cache_lifetime = 1 * 3600

#show each slide for *** seconds
slides_refresh_time = 30
