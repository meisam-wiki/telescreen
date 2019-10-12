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
import argparse
import logging
import os
import sys

from selenium import webdriver

import configs
import ci_tests
from slides import Slides

CLI_PARSER = argparse.ArgumentParser()
CLI_PARSER.add_argument(
    "-dir",
    help="directory of images",
    nargs="?",
    dest="working_directory",
    default=os.getcwd(),
)
CLI_PARSER.add_argument(
    "-w",
    "--wait",
    help="Waiting time between each slide update",
    type=int,
    dest="slides_refresh_time",
    default=30,
)
CLI_PARSER.add_argument(
    "--headless_test",
	action="store_true",
    help="Just check the generated list of the slides"
)
ARGS = CLI_PARSER.parse_args()

configs.slides_refresh_time = ARGS.slides_refresh_time
configs.working_directory = ARGS.working_directory


SLIDESHOW = Slides()

if ARGS.headless_test:
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)
    return_code = 0
    SLIDESHOW.update_slides()
    return_code += ci_tests.test_list(SLIDESHOW.list)
    sys.exit(return_code)

SLIDESHOW.browser = webdriver.Firefox()
SLIDESHOW.browser.fullscreen_window()

while True:
    SLIDESHOW.update_slides()
    SLIDESHOW.play()
