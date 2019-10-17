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
        self.wikipedia_list = []
        self.timestamp = datetime.min
        self.wikipedia_timestamp = datetime.min

        configs.cache_folder = configs.working_directory / "cache"
        configs.wikipedia_list_cache = configs.cache_folder / "wp"
        configs.local_lists_cache = configs.cache_folder / "local"

        # cleanup/create the cache directories
        configs.cache_folder.mkdir(parents=True, exist_ok=True)
        cleanup_directory(configs.cache_folder)
        configs.wikipedia_list_cache.mkdir()
        configs.local_lists_cache.mkdir()

    def update_slides(self):
        """
        update the "list" by:
            1-checking wikipedia page, caching images, adding URLs to list
            2-reading local list files, caching the images, adding URLs to list
            3-reading the local files and adding them to the list
        """
        now = datetime.now()
        if (now - self.timestamp) > configs.cache_lifetime:
            self.list = []
            self.update_from_wikipedia()

            logging.debug(
                "Updating slides from the local directory: %s",
                configs.working_directory,
            )
            cleanup_directory(configs.local_lists_cache)
            list_files = local_absolute_paths(
                configs.working_directory, configs.list_extensions
            )
            web_address = read_list_files(list_files)
            self.list += cache_images_inplace(web_address, configs.local_lists_cache)

            local_slides = local_absolute_paths(
                configs.working_directory,
                configs.img_extensions + configs.web_extensions,
            )
            self.list += [Path(slide).resolve().as_uri() for slide in local_slides]

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
            else:
                time.sleep(configs.slides_refresh_time)

    def update_from_wikipedia(self):
        """
        Checks if the wikipedia page have been updated, cleanup and cache
        otherwise, just add the URLs to the list
        """
        online_content, online_timestamp = wikipedia_source.get_lastrev()

        if online_timestamp - self.wikipedia_timestamp > timedelta():
            logging.debug("New Wikipedia list was found!")
            logging.debug(
                "wp cache timestamp: %s, live wp timestamp: %s",
                self.wikipedia_timestamp,
                online_timestamp,
            )
            cleanup_directory(configs.wikipedia_list_cache)
            self.wikipedia_list = parse_list(
                online_content,
                configs.wikipedia_lang + ":" + configs.wikipedia_list_page,
            )
            self.wikipedia_list = cache_images_inplace(
                self.wikipedia_list, configs.wikipedia_list_cache
            )
            self.list += self.wikipedia_list
            self.wikipedia_timestamp = online_timestamp
        else:
            if online_content == "":
                logging.debug("Wikipedia list was empty!")
                if self.wikipedia_list:
                    self.list += self.wikipedia_list
                    logging.debug("Local Wikipedia cache will be reused!")
            else:
                logging.debug("Wikipedia list was still valid!")
                self.list += self.wikipedia_list


def local_absolute_paths(directory, extensions_list):
    """
    returns a list of the absolute paths to the files with the given extension in
    the given directory and all of its subdirectories, excluding the cache folder
    """
    abs_paths = []
    for extension in extensions_list:
        for path in directory.glob("**/*." + extension):
            if not configs.cache_folder in path.parents:
                abs_paths.append(path.resolve())

    return abs_paths


def parse_list(text, name):
    """
    reads a string and extracts the URLs
    """
    urls = []
    for line in text.splitlines():
        new_url = line.replace("*", "").strip()
        logging.info("%s: includes: %s", name, new_url)
        urls.append(new_url)
    return urls


def parse_txt_file(file_path):
    """
    reads a local .txt file and returns the urls in the file
    """
    with file_path.open() as txt_file:
        content = txt_file.read()
    return parse_list(content, file_path)


def cache_images_inplace(urls, path):
    """
    Downloads the images in the URLs to the 'path' directory
    replaces the image URLs in the list with link to the local downloaded files
    """
    new_urls = []
    for url in urls:
        if url.endswith(configs.img_extensions):
            filename = Path(url).name
            local_path = path / filename
            try:
                wget.download(url, out=str(local_path))
            except Exception as excp:
                logging.error(str(excp) + " " + url)
            else:
                logging.debug("Downloaded %s to %s", url, local_path)
                new_urls.append(local_path.resolve().as_uri())
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


def cleanup_directory(path):
    """
    removes all the files and the subdirectories in a given path
    """
    for child in path.iterdir():
        if child.is_dir():
            cleanup_directory(child)
            child.rmdir()
        else:
            child.unlink()
