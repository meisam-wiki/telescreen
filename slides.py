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
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import wget

import configs
import wikipedia_source


class Slides:
    """
    Slideshow class
    """

    browser = None

    def __init__(self):
        self.list = []
        self.timestamp = 0.0
        self.wikipedia_timestamp = datetime.min

        working_directory = Path(configs.working_directory)
        configs.cache_folder = working_directory / "cache"
        configs.wikipedia_list_cache = configs.cache_folder / "wp"
        configs.local_lists_cache = configs.cache_folder / "local"
        configs.wikipedia_listfile = (
            configs.wikipedia_list_cache / "wikipedia_listfile.txt"
        )

        # cleanup the cache directories and the temp files
        if not os.path.isdir(configs.cache_folder):
            os.mkdir(configs.cache_folder)
        if os.path.isdir(configs.wikipedia_list_cache):
            cleanup_directory(configs.wikipedia_list_cache)
        else:
            os.mkdir(configs.wikipedia_list_cache)
        if os.path.isdir(configs.local_lists_cache):
            cleanup_directory(configs.local_lists_cache)
        else:
            os.mkdir(configs.local_lists_cache)
        if os.path.isfile(configs.wikipedia_listfile):
            os.remove(os.path.abspath(configs.wikipedia_listfile))

    def update_slides(self):
        """
        update the "list" by:
            1-checking wikipedia page, caching images, adding URLs to list
            2-reading local list files, caching the images, adding URLs to list
            3-reading all the local and cached images and adding them to the list
        """
        now = time.time()
        if (now - self.timestamp) > configs.cache_lifetime:
            self.list = []
            self.update_from_wikipedia()

            logging.debug(
                "Updating slides from the local directory: %s",
                configs.working_directory,
            )
            cleanup_directory(configs.local_lists_cache)
            list_files = local_lists_path(configs.working_directory)
            web_address = read_list_files(list_files)
            self.list += cache_images(web_address, configs.local_lists_cache)

            local_slides = local_files_path(configs.working_directory)
            self.list += local_urls(local_slides)

            self.timestamp = now
            logging.debug("Final slides list: %s", self.list)

    def play(self):
        """
        loads the slide urls from the list one-by-one into the browser
        """
        for url in self.list:
            try:
                self.browser.get(url)
            except Exception as exc:
                logging.warning("Couldn't load the url: %s", str(exc))
            time.sleep(configs.slides_refresh_time)

    def update_from_wikipedia(self):
        """
        Checks if the wikipedia page have been updated, cleanup and cache
        otherwise, just add the URLs to the list
        """
        online_context, online_timestamp = wikipedia_source.get_lastrev()

        if online_timestamp - self.wikipedia_timestamp > timedelta():
            logging.debug("New Wikipedia list was found!")
            logging.debug(
                "local wp timestamp: %s, New wp timestamp: %s",
                self.wikipedia_timestamp,
                online_timestamp,
            )
            cleanup_directory(configs.wikipedia_list_cache)
            update_wikipedia_listfile(online_context)
            wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
            self.list += cache_images(wikipedia_list, configs.wikipedia_list_cache)
            self.wikipedia_timestamp = online_timestamp
        else:
            if online_context == "":
                cleanup_directory(configs.wikipedia_list_cache)
                logging.debug("Wikipedia list was empty!")
            else:
                logging.debug("Wikipedia list was still valid!")
                wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
                self.list += web_links(wikipedia_list)


def local_files_path(input_dir="."):
    """
    returns a list of the absolute paths to the slide files in the
    input directory and all of its subdirectories, excluding cache folders
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        if Path(root) == configs.cache_folder:
            continue
        for file in sorted(files):
            if file.endswith(configs.img_extensions + configs.web_extensions):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)

    return paths


def local_lists_path(input_dir="."):
    """
    returns a list of the absolute paths to the txt files in the input directory
    and all of its subdirectories except the wikipedia list file
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(configs.list_extensions):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)

    if os.path.abspath(configs.wikipedia_listfile) in paths:
        paths.remove(os.path.abspath(configs.wikipedia_listfile))
    return paths


def local_urls(absolute_file_paths):
    """
    generates a list of the urls from the list of the absolute paths
    to the local files
    """
    urls = []
    for path in absolute_file_paths:
        if path.endswith(configs.img_extensions + configs.web_extensions):
            urls.append("file://" + path)
    return urls


def parse_txt_file(file_path):
    """
    reads a local .txt file and returns the urls in the file
    """
    urls = []
    with open(file_path, "r") as txt_file:
        txtfile_lines = txt_file.readlines()
    for line in txtfile_lines:
        new_url = line.replace("*", "").strip()
        logging.info("%s: includes: %s", file_path, new_url)
        urls.append(new_url)
    return urls


def cache_images(urls, path):
    """
    Downloads the images in the URLs to the 'path' directory
    """
    new_urls = []
    for url in urls:
        if url.endswith(configs.img_extensions):
            filename = os.path.basename(url)
            local_path = os.path.join(path, filename)
            try:
                wget.download(url, out=local_path)
                logging.debug("Downloaded %s to %s", url, local_path)
            except Exception as excp:
                logging.error(str(excp) + " " + url)
            else:
                new_urls.append(local_path)
        else:
            new_urls.append(url)
    return new_urls


def read_list_files(list_files):
    """
    parses all the text files and returns the content
    """
    urls = []
    for file in list_files:
        urls += parse_txt_file(file)

    return urls


def web_links(urls):
    """
    removes the image URLs and returns only the web links
    """
    for url in urls:
        if url.endswith(configs.img_extensions):
            urls.remove(url)

    return urls


def update_wikipedia_listfile(context):
    """
    gets the content of the wikipedia page and puts it inside a text file
    """

    with open(configs.wikipedia_listfile, "w") as file:
        file.write(context)

    if os.path.isfile(configs.wikipedia_listfile):
        if os.path.getsize(configs.wikipedia_listfile) > 0:
            logging.debug("Wikipedia page has been successfully downloaded!")
    else:
        logging.error("Couldn't write the %s to the disk!", configs.wikipedia_listfile)


def cleanup_directory(path):
    """
    removes all the files in the directory
    """
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
