FROM kpavlovsky/python3.7

WORKDIR /opt/shakkelha_server

RUN git clone https://github.com/AliOsm/shakkelha.git /opt/shakkelha

COPY . .

RUN pip3 install -U setuptools

RUN pip3 install -r shakkelha_server_requirements.txt

CMD ["python3","manage.py","runserver","0.0.0.0:8080"]