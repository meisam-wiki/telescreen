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

import configs

def test_list(generated_slides_list):
    """
    compares the generated_slides_list to its hardcoded test_slides_list
    returns 0 if both lists are equivalent, otherwise returns 1
    """
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
        print("\nHurrah! The generated slides list is correct.")
        return 0
    else:
        print("\nERROR: The generated slides list is not the same as the reference list!")
        print("Test reference slides list: ", test_slides_list)
        print("Generated slides list: ", generated_slides_list)
        return 1
    