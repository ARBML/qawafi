FROM kpavlovsky/python3.7

WORKDIR /opt/qawafi_server

COPY qawafi_server_requirements.txt qawafi_server_requirements.txt

RUN pip3 install -U pip

RUN pip3 install -U setuptools

RUN pip3 install -r qawafi_server_requirements.txt

COPY . .

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]