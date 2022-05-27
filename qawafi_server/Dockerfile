FROM kpavlovsky/python3.7

WORKDIR /opt/qawafi_server

COPY . .

RUN pip3 install -U pip

RUN pip3 install -U setuptools

RUN pip3 install -r qawafi_server_requirements.txt

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]