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
import argparse
import os
from selenium import webdriver
import slides
import configs

CLI_PARSER = argparse.ArgumentParser()
CLI_PARSER.add_argument('-dir',
                        help='directory of images',
                        nargs='?',
                        dest='working_directory',
                        default=os.getcwd())
CLI_PARSER.add_argument('-w', '--wait',
                        help='Waiting time between each slide update',
                        type=int,
                        dest='slides_refresh_time',
                        default=30)
ARGS = CLI_PARSER.parse_args()

configs.slides_refresh_time = ARGS.slides_refresh_time
configs.working_directory = ARGS.working_directory


SLIDESHOW = slides.Slides()
SLIDESHOW.browser = webdriver.Firefox()
SLIDESHOW.browser.fullscreen_window()

while True:
    SLIDESHOW.update_slides()
    SLIDESHOW.play()
