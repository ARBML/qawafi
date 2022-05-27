import requests
import random
import sys
import time
import json

sys.path.append("..")
sys.path.append("../qawafi_server")
from bohour.poem_samples_large import samples

random.seed(1)

qasaed = [random.choice(samples) for _ in range(10)]
from pprint import pprint

for qaseeda in qasaed:
    print(qaseeda, type(qaseeda))
    response = requests.post(
        "http://127.0.0.1:8080/api/diacritize",
        data={"baits": json.dumps(qaseeda, ensure_ascii=False)},
    )
    time.sleep(5)
    if response.ok:
        pprint(response.text)
