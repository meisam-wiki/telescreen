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

import configs

def test_list(generated_slides_list):
    """
    compares the generated_slides_list to its hardcoded test_slides_list
    returns 0 if both lists are equivalent, otherwise returns 1
    """
    print("Checking Telescreen slides list generation.")
    test_slides_list = ["https://www.wikidata.org/?uselang=de", #from wikipedia
                        "https://commons.wikimedia.org/?uselang=de", #from wikipedia
                        "https://de.wikipedia.org", #from wikipedia
                        (configs.wikipedia_list_cache / "2000px-Strategy_Graphic_-_High_level.svg.png").resolve().as_uri(), #from wikipedia
                        "https://darksky.net/forecast/48.1521,11.5445/ca24/de", # form ./test/test_list.txt
                        "https://www.wikipedia.org", # form ./test/test_list.txt
                        (configs.local_lists_cache / "WikiMUC_Garamond2.jpg").resolve().as_uri(), # form ./test/test_list.txt
                        (configs.working_directory / "Angertorstr._3_mit_WikiMUC_bearbeitet.jpg").resolve().as_uri(), # form ./test/*
                       ]

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

def test_cache_renewal(slideshow):
    """
    changes the timestamp of the slideshow and checks the updating of
    cache after sometime before and after the cache lifetime
    """
    print("Checking Telescreen cache renewal.")
    slideshow.timestamp = datetime.now()
    slideshow.timestamp -= configs.cache_lifetime - timedelta(seconds=10)
    initial_timestamp = slideshow.timestamp
    slideshow.update_slides()

    if initial_timestamp != slideshow.timestamp:
        print("\033[31m" + "ERROR: The slides list got updated prematurely!" + "\033[0m")
        print("cache_lifetime: ", configs.cache_lifetime)
        print("Tested update interval: ", configs.cache_lifetime - timedelta(seconds=10))
        print("initial timestamp: ", initial_timestamp)
        print("new timestamp: ", slideshow.timestamp)
        return 1

    slideshow.timestamp = datetime.now()
    slideshow.timestamp -= configs.cache_lifetime + timedelta(seconds=1)
    initial_timestamp = slideshow.timestamp
    slideshow.update_slides()

    if initial_timestamp == slideshow.timestamp:
        print("\033[31m" + "ERROR: The slides list did not get updated after the cache_lifetime!" + "\033[0m")
        print("cache_lifetime: ", configs.cache_lifetime)
        print("Tested update interval: ", configs.cache_lifetime + timedelta(seconds=1))
        return 1

    print("\033[32m" + "Huzzah! Slideshow cache update is working as expected!" + "\033[0m")
    return 0
