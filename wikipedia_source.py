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
import requests
import configs

def get():
    """
    Returns the content of the latest revision of the "configs.wikipedia_list_page" page
    which has been edited by a whitelisted user
    """
    url = "https://" + configs.wikipedia_lang + ".wikipedia.org/w/api.php"
    query = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "list": "",
        "titles": configs.wikipedia_list_page,
        "rvprop": "timestamp|ids|user|content",
        "rvlimit": "max"
    }

    result = requests.get(url, params=query)
    data = result.json()
    pageid = list(data["query"]["pages"].keys())[0]
    revisions = data["query"]["pages"][pageid]["revisions"]
    for i, rev in enumerate(revisions):
        if rev['user'] in configs.whitelist_users:
            return rev['*']
        else:
            logging.debug("User %s is NOT whitelisted!", rev['user'])

    logging.warning("Couldn't find any revisions from the Wikipedia page \"%s\""
                    "which is edited by the whitelisted users!", configs.wikipedia_list_page)
    return ''
