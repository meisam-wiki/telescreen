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


#import sys
import os
import time
import logging
import wget
import configs
import wikipedia_source


class Slides:
    """
    Slideshow class
    """
    start_time = time.time()
    browser = None
    def __init__(self):
        self.list = []
        self.timestamp = 0.0
        logging.basicConfig(filename='telescreen.log', level=logging.DEBUG)
        configs.downloads_directory = configs.working_directory + "/cache"
        if not os.path.isdir(configs.downloads_directory):
            os.mkdir(configs.downloads_directory)

    def update_slides(self):
        """
        update the "list" by:
        cleaning the download cache directory
        put the content of the wikipedia page in a local text file
        generate the list from the files in the local directory
        """
        now = time.time()
        if (now - self.timestamp) > configs.cache_lifetime:
            cleanup_directory(configs.downloads_directory)
            update_wikipedia_listfile()
            local_paths = local_file_paths(configs.working_directory)
            logging.debug('Updating slides from: %s', configs.working_directory)
            self.list = generate_urls(local_paths)
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

#    def update_script(self):
#        now = time.time()
#        if (now - self.start_time) > configs.script_lifetime:
#            self.browser.close()
#            #TODO: git clone the master branch
#            logging.debug('Time now=' + str(now))
#            logging.debug('Restarting the Telescreen!')
#            os.execl(sys.executable, *([sys.executable] + sys.argv))

def update_wikipedia_listfile():
    """
    get the content of the wikipedia page and put in inside a text file
    """
    local_listfile = configs.working_directory + '/wikipedia_listfile.txt'
    context = wikipedia_source.get()
    file = open(local_listfile, "w")
    file.write(context)
    file.close()

    if os.path.isfile(local_listfile):
        if os.path.getsize(local_listfile) > 0:
            logging.debug('Wikipedia page is downloaded!')
    else:
        logging.error("Couldn't write the %s to the disk!", local_listfile)




def local_file_paths(input_dir='.'):
    """
    returns a list of the absolute paths to the images/html/txt files in the input directory
    and all of its subdirectories
    """
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif', 'htm', 'html', 'txt')):
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
        if path.endswith(('jpg', 'png', 'gif', 'htm', 'html')):
            urls.append('file://' + path)
        elif path.endswith(('txt')):
            urls += urls_in_local_txt_file(path)
    return urls



def urls_in_local_txt_file(txtfile_path):
    """
    reads a local .txt file and downloads the images to
    the cache directory or returns the urls in the file
    """
    urls = []
    txt_file = open(txtfile_path, "r")
    txtfile_lines = txt_file.readlines()
    for line in txtfile_lines:
        new_url = line.replace('*', '').strip()
        logging.info(txtfile_path + ': New slide found: ' + new_url)
        if new_url.endswith(('jpeg', 'jpg', 'png', 'gif')):
            try:
                filename = os.path.basename(new_url)
                local_path = configs.downloads_directory + '/' + filename
                wget.download(new_url, out=local_path)
                urls.append('file://' + os.path.abspath(local_path))
            except Exception as excp:
                logging.error(str(excp) + ' ' + new_url)
                urls.append(new_url)
        else:
            urls.append(new_url)
    return urls


def cleanup_directory(path):
    """
    removes all the files in the path directory
    """
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))
