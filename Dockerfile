FROM python:3

ADD main.py README.md requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
