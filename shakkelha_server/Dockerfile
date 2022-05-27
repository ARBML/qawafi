FROM kpavlovsky/python3.7

WORKDIR /opt/shakkelha_server

COPY shakkelha_server_requirements.txt shakkelha_server_requirements.txt

RUN pip3 install -U setuptools

RUN pip3 install -r shakkelha_server_requirements.txt

RUN git clone https://github.com/AliOsm/shakkelha.git /opt/shakkelha

COPY . .

CMD ["python3","manage.py","runserver","0.0.0.0:8080"]
