[![Build Status](https://travis-ci.com/meisam-wiki/telescreen.svg?branch=master)](https://travis-ci.com/meisam-wiki/telescreen)
## Telescreen
A Simple Slideshow for the [WikiMUC](https://de.wikipedia.org/wiki/Wikipedia:WikiMUC)

### Introduction
Telescreen is a simple slideshow python script. It can display images and webpages from multiple sources including:
* Files (.png, .jpg, .jpeg, .gif, .html, .htm) in the local directory
* URLs inside a text file in the local directory
* URLs in a Wikipedia page

By default the images found in the URL lists will be locally cached.

### Installation
Telescreen uses [Selenium](https://github.com/SeleniumHQ/selenium/) to control a local web browser. It also depends on the wget python package to download the images and cache them locally.
You can simply install these using the Python's package installer (pip) as:

```sh
$ sudo apt-get install python3 pip3
$ pip3 install selenium wget
```
In addition, the Telescreen (through the Selenium) requires a browser and its compatible webdriver to work.
A tested version of the webdriver for the Firefox (geckodriver) has been included in the “./geckodriver/”. You have to extract the compressed binary for your OS and add it to your system path. To build the geckodriver from the source for a different OS, please refer to the [geckodriver build manual](https://firefox-source-docs.mozilla.org/testing/geckodriver/Building.html).
You can download the latest version of the geckodriver from [here](https://github.com/mozilla/geckodriver/releases/latest)!
To use the Telescreen with a different browser please follow the instructions on the [Selenium guide page](https://pypi.org/project/selenium/).

### Configurations
You can edit the configs.py and change the default parameters of Telescreen. This includes the default:
- directory of the slides, and slides cache
- Address of the Wikipedia page containing the URLs and the whitelisted users allowed to modify the page
- Cache lifetime
- Slides refresh time

### Adding slides
You can add slides by either putting images/webpages in the working directory, creating a .txt file with each URL in a newline, or adding the URLs to a Wikipedia page by the whitelisted user accounts. (URLS are allowed to start with “*”) 
The contents of the Wikipedia page will be automatically put into the “wikipedia_listfile.txt” file in the working directory and parsed from there.

### Execution
```sh
$ python3 telescreen.py -dir ./test/ -w 20
```
  - -dir: Path to the local directory containing the slides
  - -w: Slides refresh time. Delay time (in seconds) between changing the slides

### License and attributions

* source: Telescreen source is available under the [GNU GPL v3+] (attributions: Meisam@wikimedia, MichaelSchoenitzer@wikimedia)
* test slides: The copyright of each image in the ./test directory belongs to its original author. Please refer to the ./test/README file for more information.
* geckodriver: The geckodriver is made available under the [Mozilla Public License].

[GNU GPL v3+]: https://www.gnu.org/licenses/quick-guide-gplv3.html
[Mozilla Public License]: https://www.mozilla.org/en-US/MPL/2.0/
