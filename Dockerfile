FROM python:3

WORKDIR /python-crawler/

ADD main.py requirements.txt test_crawler.py python_crawler.py ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "main.py"]
