FROM python:3

ADD main.py requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "main.py"]
