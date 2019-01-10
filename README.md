# python-crawler for website https://wiprodigital.com/
IMPORTANT: This is a demo and the program was only tested on a single webpage (https://wiprodigital.com/), most likely won't work on other sites due to different xpath expressions.

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


