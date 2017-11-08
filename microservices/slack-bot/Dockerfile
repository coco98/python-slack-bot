FROM python:3.5.2-alpine

WORKDIR /usr/src/

COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY src /usr/src

CMD ["python", "-u", "job.py"]
