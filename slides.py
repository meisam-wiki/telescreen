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

import os
import time
import logging
from datetime import datetime
from datetime import timedelta
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

        configs.wikipedia_cache = configs.working_directory + "/cache/wp"
        configs.lists_cache = configs.working_directory + "/cache/local"
        configs.wikipedia_listfile = configs.wikipedia_cache + '/wikipedia_listfile.txt'

        #cleanup the directory and the temp files
        if os.path.isdir(configs.wikipedia_cache):
            cleanup_directory(configs.wikipedia_cache)
        else:
            os.mkdir(configs.wikipedia_cache)
        if os.path.isdir(configs.lists_cache):
            cleanup_directory(configs.lists_cache)
        else:
            os.mkdir(configs.lists_cache)
        if os.path.isfile(configs.wikipedia_listfile):
            os.remove(os.path.abspath(configs.wikipedia_listfile))

    def update_slides(self):
        """
        update the "list" by:
        cleaning the download cache directories
        put the content of the wikipedia page in a local text file
        generate the list from the files in the local directory
        """
        now = time.time()
        if (now - self.timestamp) > configs.cache_lifetime:
            self.list = []
            self.update_from_wikipedia()
            cleanup_directory(configs.lists_cache)
            local_slides = local_slide_paths(configs.working_directory)
            logging.debug('Updating slides from: %s', configs.working_directory)
            self.list += local_urls(local_slides)
            list_files = local_list_paths(configs.working_directory)
            web_address = read_list_files(list_files)
            cache_images(web_address, configs.lists_cache)
            cached_files = local_slide_paths(configs.lists_cache)
            self.list += local_urls(cached_files)
            self.timestamp = now
            logging.debug('Final slide list: %s', self.list)

    def play(self):
        """
        loads the slide urls from the list one-by-one
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
        """
        online_context, online_timestamp = wikipedia_source.get_lastrev()
        #newer revision has been found!
        if online_timestamp - self.wikipedia_timestamp > timedelta():
            cleanup_directory(configs.wikipedia_cache)
            update_wikipedia_listfile(online_context)
            wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
            cache_images(wikipedia_list, configs.wikipedia_cache)
            self.list += web_links(wikipedia_list)
            logging.debug('Wikipedia list renewed!')
            logging.debug('local timestamp: %s, New timestamp: %s', 
                          self.wikipedia_timestamp, online_timestamp)
            self.wikipedia_timestamp = online_timestamp
        else:
            #invalid online revision
            if online_context == '':
                cleanup_directory(configs.wikipedia_cache)
                logging.debug('Wikipedia list was empty!')
            #old revision is still valid
            #(Will reuse the cached images, only add the links to the list)
            else:
                wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
                self.list += web_links(wikipedia_list)
                logging.debug('Wikipedia list was still valid!')



def local_slide_paths(input_dir='.'):
    """
    returns a list of the absolute paths to the images/html files in the input directory
    and all of its subdirectories excluding caches
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if (not configs.wikipedia_cache in file) and (not configs.lists_cache in file):
                if file.endswith(configs.extensions_img+configs.extensions_web+configs.extensions_list):
                    path = os.path.abspath(os.path.join(root, file))
                    paths.append(path)

    return paths


def local_list_paths(input_dir='.'):
    """
    returns a list of the absolute paths to the txt files in the input directory
    and all of its subdirectories except the wikipedia list file
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(configs.extensions_list):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)

    if os.path.abspath(configs.wikipedia_listfile) in paths:
        paths.remove(os.path.abspath(configs.wikipedia_listfile))
    return paths


def local_urls(absolute_file_paths):
    """
    generates a list of the urls from the list of the absolute paths
    to the local files.
    """
    urls = []
    for path in absolute_file_paths:
        if path.endswith(configs.extensions_img + configs.extensions_web):
            urls.append('file://' + path)
    return urls



def parse_txt_file(file_path):
    """
    reads a local .txt file and downloads the images to
    the cache directory or returns the urls in the file
    """
    urls = []
    txt_file = open(file_path, "r")
    txtfile_lines = txt_file.readlines()
    for line in txtfile_lines:
        new_url = line.replace('*', '').strip()
        logging.info(file_path + ': New slide found: ' + new_url)
        urls.append(new_url)
    return urls


def cache_images(urls, path):
    """
    checks for the images in the URLs and tries to download them
    """
    for url in urls:
        if url.endswith(configs.extensions_img):
            try:
                filename = os.path.basename(url)
                local_path = path + '/' + filename
                wget.download(url, out=local_path)
                logging.debug('Downloaded %s to %s', url, local_path)
            except Exception as excp:
                logging.error(str(excp) + ' ' + url)

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
        if url.endswith(configs.extensions_img):
            urls.remove(url)

    return urls

def update_wikipedia_listfile(context):
    """
    gets the content of the wikipedia page and puts it inside a text file
    """

    file = open(configs.wikipedia_listfile, "w")
    file.write(context)
    file.close()

    if os.path.isfile(configs.wikipedia_listfile):
        if os.path.getsize(configs.wikipedia_listfile) > 0:
            logging.debug('Wikipedia page has been successfully downloaded!')
    else:
        logging.error("Couldn't write the %s to the disk!", configs.wikipedia_listfile)


def cleanup_directory(path):
    """
    removes all the files in the directory
    """
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
