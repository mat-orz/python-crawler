# python-crawler for website https://wiprodigital.com/
IMPORTANT: This is a demo and the program was only tested on a single webpage, most likely won't work on other sites due to different xpath expressions. Do not use on any production systems.

Python crawler that given url visits all local links recusively and gathers links to images, css, js and external url references. 
The output of the crawler will be a pseudo sitemap in json format.


## Requirements

Docker or if run locally:

```
Python 3
pip
```


## Usage

Docker

```
git clone https://github.com/mat-orz/python-crawler.git
chmod +x run_as_docker_image.sh
./run_as_docker_image.sh
```

You can modify run_as_docker_image.sh variables to have different image name, url or final output name:
```
IMAGE_NAME="python-crawler-mat-orz"
URL="https://wiprodigital.com"
OUT_FILE="sitemap.json"
```

Python 3 (virtualenv)

```
git clone https://github.com/mat-orz/python-crawler.git
python -m venv python-crawler/
source python-crawler/bin/activate
cd python-crawler
pip install -r requirements.txt
python main.py "https://wiprodigital.com/" "<some_name>"
```


## Output

The final json will be stored in the output/<some_name>

## Project Notes

- Could have used BeautifulSoup or Scrapy for the crawling part but wanted to avoid unnecessary overhead. Used scrapy shell to test the xpaths. 
  The pros of this approach is that the logic is clear, the cons is that it took some more time to develop.

- The program is meant just for the https://wiprodigital.com/ site, (most likely) won't work with other sites due to different xpaths. 

## Things to do with more time

- Unit tests.
- Catching possible exceptions.
- Better argument parser (debug and test variables) and config file (mainly for xpaths).
- Don't like the main logic of the crawler, could be done as a recursive function.
- More robust xpaths to cover all cases so it can be used on other sites as well.
- More human readable sitemap, possibly as a graph (graphviz?).
- Fix TODOs from the source code comments

