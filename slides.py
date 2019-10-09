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
        logging.basicConfig(filename='telescreen.log', level=logging.DEBUG)

        configs.wikipedia_cache = configs.working_directory + "/wp_cache"
        configs.lists_cache = configs.working_directory + "/cache"
        configs.wikipedia_listfile = configs.wikipedia_cache + '/wikipedia_listfile.txt'

        if not os.path.isdir(configs.wikipedia_cache):
            os.mkdir(configs.wikipedia_cache)
        if not os.path.isdir(configs.lists_cache):
            os.mkdir(configs.lists_cache)

    def update_slides(self):
        """
        update the "list" by:
        cleaning the download cache directories
        put the content of the wikipedia page in a local text file
        generate the list from the files in the local directory
        """
        now = time.time()
        if (now - self.timestamp) > configs.cache_lifetime:
            self.update_wikipedia()
            cleanup_directory(configs.lists_cache)
            local_paths = local_file_paths(configs.working_directory)
            print(local_paths)
            if os.path.isfile(configs.wikipedia_listfile):
                local_paths.remove(os.path.abspath(configs.wikipedia_listfile))
            logging.debug('Updating slides from: %s', configs.working_directory)
            locallist = generate_urls(local_paths)
            self.list = cache_images(locallist, configs.lists_cache)
            self.timestamp = now

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

    def update_wikipedia(self):
        """
        Checks if the wikipedia page have been updates, cleanup and cache
        """
        context, timestamp = wikipedia_source.get_lastrev()
        #Newer revision is found!
        if timestamp - self.wikipedia_timestamp > timedelta():
            cleanup_directory(configs.wikipedia_cache)
            update_wikipedia_listfile(context)
            wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
            self.list += cache_images(wikipedia_list, configs.wikipedia_cache)
        else:
            #invalid rev
            if context == '':
                cleanup_directory(configs.wikipedia_cache)
            #old revision is still valid
            else:
                wikipedia_list = parse_txt_file(configs.wikipedia_listfile)
                self.list += remove_images(wikipedia_list)



def local_file_paths(input_dir='.'):
    """
    returns a list of the absolute paths to the images/html/txt files in the input directory
    and all of its subdirectories
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(configs.extensions_img+configs.extensions_web+configs.extensions_list):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths



def generate_urls(paths):
    """
    generates a list of the urls from the list of the absolute paths
    to the local files. The text files are parsed as 1-url per line
    """
    urls = []
    for path in paths:
        if path.endswith(configs.extensions_img + configs.extensions_web):
            urls.append('file://' + path)
        elif path.endswith(('txt')):
            urls += parse_txt_file(path)
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
                urls.append('file://' + os.path.abspath(local_path))
                urls.remove(url)
            except Exception as excp:
                logging.error(str(excp) + ' ' + url)
    return urls


def remove_images(urls):
    """
   removes the images in the from the URLs (already cached!)
    """
    for url in urls:
        if url.endswith(configs.extensions_img):
            urls.remove(url)

    return urls

def update_wikipedia_listfile(context):
    """
    get the content of the wikipedia page and put in inside a text file
    """

    file = open(configs.wikipedia_listfile, "w")
    file.write(context)
    file.close()

    if os.path.isfile(configs.wikipedia_listfile):
        if os.path.getsize(configs.wikipedia_listfile) > 0:
            logging.debug('Wikipedia page is downloaded!')
    else:
        logging.error("Couldn't write the %s to the disk!", configs.wikipedia_listfile)


def cleanup_directory(path):
    """
    removes all the files in the path directory
    """
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
