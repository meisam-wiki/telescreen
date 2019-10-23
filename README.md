[![Build Status](https://travis-ci.com/meisam-wiki/telescreen.svg?branch=master)](https://travis-ci.com/meisam-wiki/telescreen)
[![Coverage Status](https://coveralls.io/repos/github/meisam-wiki/telescreen/badge.svg?branch=master)](https://coveralls.io/github/meisam-wiki/telescreen?branch=master)
![Python Version](https://img.shields.io/badge/python-%3E%3D3.5-blue)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![License: GPL v3+](https://img.shields.io/badge/License-GPLv3+-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
## Telescreen
A simple image & web-page slideshow for the [WikiMUC](https://de.wikipedia.org/wiki/Wikipedia:WikiMUC)

### Introduction
Telescreen is a simple slideshow python script. It can display images and webpages from multiple sources including:
* Files (.png, .jpg, .jpeg, .gif, .html, .htm) in the local directory
* URLs inside a text file in the local directory
* URLs in a Wikipedia page

By default the images found in the URL lists will be locally cached.

### Installation
Telescreen uses [Selenium](https://github.com/SeleniumHQ/selenium/) to control a local web browser. It also depends on the [requests](https://pypi.org/project/requests/) python package to load the wikipedia pages, and [wget](https://pypi.org/project/wget/) package to download the images and cache them locally.
You can simply install the tested versions of these packages using the Python's package installer (pip) as:

```sh
$ sudo apt-get install python3 pip3
$ pip3 install -r requirements.txt
```
In addition, the Telescreen (through the Selenium) requires a browser and its compatible webdriver to work.
A tested version of the webdriver for the Firefox (geckodriver) has been included in the “./geckodriver/”. You have to extract the compressed binary for your OS and add it to your system path. 

To build the geckodriver from the source for a different OS, please refer to the [geckodriver build manual](https://firefox-source-docs.mozilla.org/testing/geckodriver/Building.html). You can download the latest version of the geckodriver from [here](https://github.com/mozilla/geckodriver/releases/latest)!

To use the Telescreen with a different browser please follow the instructions on the [Selenium guide page](https://pypi.org/project/selenium/). (You will also have to change the “SLIDESHOW.browser” parameter in the “telescreen.py” file)

### Configurations
You can edit the configs.py and change the default parameters of Telescreen. This includes the default:
- Directory of the slides, and slides cache
- Address of the Wikipedia page containing the URLs and the list of the users allowed to modify it
- Cache lifetime
- Slides refresh time

### Adding slides
You can add slides by either putting images/webpages in the working directory, creating a .txt file with each URL in a newline, or adding the URLs to a Wikipedia page by the whitelisted user accounts. (the URLs are allowed to start with “*”)

### Execution
* Run the Telescreen with the default value for the parameters as defined in the configs.py
```sh
$ python3 telescreen.py
```

* Show the available command line switches
```sh
$ python3 telescreen.py --help
```

* Run the Telescreen with slide files in ./test/ directory and show each slide for 20 seconds
```sh
$ python3 telescreen.py -dir ./test/ -w 20
```

### Troubleshooting
By default, the Telescreen logs all the messages to “telescreen.log” file. You can use this file for monitoring the events or for its troubleshooting. The logging behavior of the Telescreen can be tweaked in the configs.py file.

### License and attributions

* source: Telescreen source is available under the [GNU GPL v3+] (attributions: Meisam@wikimedia, MichaelSchoenitzer@wikimedia)
* test slides: The copyright of each image in the ./test directory belongs to its original author. Please refer to the ./test/README file for more information.
* geckodriver: The geckodriver is made available under the [Mozilla Public License].

[GNU GPL v3+]: https://www.gnu.org/licenses/quick-guide-gplv3.html
[Mozilla Public License]: https://www.mozilla.org/en-US/MPL/2.0/
