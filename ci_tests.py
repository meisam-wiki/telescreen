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

from datetime import datetime, timedelta
from pathlib import Path

from slides import Slides
import configs

def test_list():
    """
    compares the generated_slides_list to its hardcoded test_slides_list
    returns 0 if both lists are equivalent, otherwise returns 1
    """
    print("Checking Telescreen slides list generation.")

    configs.working_directory = Path('./test')

    #this file shouldn't be in the final list
    invalid_file_type = configs.working_directory / "yolo.zif"
    invalid_file_type.open('w').write('something!')

    slideshow = Slides()
    slideshow.update_slides()

    test_slides_list = ["https://www.wikidata.org/?uselang=de", #from wikipedia
                        "https://commons.wikimedia.org/?uselang=de", #from wikipedia
                        "https://de.wikipedia.org", #from wikipedia
                        (configs.wikipedia_list_cache / "2000px-Strategy_Graphic_-_High_level.svg.png").resolve().as_uri(), #from wikipedia
                        "https://darksky.net/forecast/48.1521,11.5445/ca24/de", # form ./test/test_list.txt
                        "https://www.wikipedia.org", # form ./test/test_list.txt
                        (configs.local_lists_cache / "WikiMUC_Garamond2.jpg").resolve().as_uri(), # form ./test/test_list.txt
                        (configs.working_directory / "Angertorstr._3_mit_WikiMUC_bearbeitet.jpg").resolve().as_uri(), # form ./test/*
                       ]

    generated_slides_list = slideshow.list
    generated_slides_list.sort()
    test_slides_list.sort()

    if generated_slides_list == test_slides_list:
        print("\033[32m" + "Hurrah! The generated slides list is correct." + "\033[0m")
        return 0
    else:
        print("\033[31m" + "ERROR: The generated slides list is not the same as the reference list!" + "\033[0m")
        print("Test reference slides list: ", test_slides_list)
        print("Generated slides list: ", generated_slides_list)
        return 1

def test_cache_renewal():
    """
    changes the timestamp of the slideshow and checks the updating of
    cache after sometime before and after the cache lifetime
    """
    print("Checking Telescreen cache renewal.")
    configs.working_directory = Path('./test')
    slideshow = Slides()

    timeshift = configs.cache_lifetime - timedelta(seconds=10)
    slideshow.timestamp = datetime.now() - timeshift
    shifted_timestamp = slideshow.timestamp
    slideshow.update_slides()

    if shifted_timestamp != slideshow.timestamp:
        print("\033[31m" + "ERROR: The slides list got updated prematurely!" + "\033[0m")
        print("cache_lifetime: ", configs.cache_lifetime)
        print("Tested time shift: ", timeshift)
        print("shifted timestamp: ", shifted_timestamp)
        print("new timestamp: ", slideshow.timestamp)
        return 1

    timeshift = configs.cache_lifetime + timedelta(seconds=1)
    slideshow.timestamp = datetime.now() - timeshift
    shifted_timestamp = slideshow.timestamp
    slideshow.update_slides()

    if shifted_timestamp == slideshow.timestamp:
        print("\033[31m" + "ERROR: The slides list did not get updated after the cache_lifetime!" + "\033[0m")
        print("cache_lifetime: ", configs.cache_lifetime)
        print("Tested time shift: ", timeshift)
        print("shifted timestamp: ", shifted_timestamp)
        return 1

    print("\033[32m" + "Huzzah! slideshow cache update is working as expected!" + "\033[0m")
    return 0

def test_errors():
    """
    checks the exception handling in the code
    """
    print("Checking Telescreen error handling.")

    print("Testing invalid working directory.")
    configs.working_directory = Path('./invalid_path_420/deeper_level')
    try:
        slideshow = Slides()
    except Exception as exc:
        print("\033[31m" + "ERROR: Couldn’t initialize the Telescreen with an invalid working directory: " + str(exc) + "\033[0m")
        return 1

    configs.wikipedia_list_cache.rmdir()
    configs.local_lists_cache.rmdir()
    configs.cache_folder.rmdir()
    configs.working_directory.rmdir() #./invalid_path_420/deeper_level
    configs.working_directory.parent.rmdir() #./invalid_path_420
    configs.working_directory = Path('./test')


    print("Testing no wikipedia revision by the whitelisted users.")
    configs.whitelist_users = ["Jimbo Wales"]
    try:
        slideshow = Slides()
        slideshow.update_slides()
    except Exception as exc:
        print("\033[31m" + "ERROR: Couldn’t initialize the Telescreen with no revision from the whitelisted users: " + str(exc) + "\033[0m")
        return 1

    configs.whitelist_users = ["Meisam"]


    print("Testing invalid Wikipedia page.")
    configs.wikipedia_list_page = "Benutzer:Meisam/invalid_page_420"
    try:
        slideshow = Slides()
        slideshow.update_slides()
    except Exception as exc:
        print("\033[31m" + "ERROR: Couldn’t initialize the Telescreen with an invalid Wikipedia page: " + str(exc) + "\033[0m")
        return 1

    configs.wikipedia_list_page = "Benutzer:Meisam/test"


    print("\033[32m" + "Whoopee! All the tested exceptions are being handled!" + "\033[0m")
    return 0
 