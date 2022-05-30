import json
import random
import sys
import time
from pprint import pprint

import requests

sys.path.append("..")
from bohour.poem_samples_large import samples


random.seed(1)

qasaed = [random.choice(samples) for _ in range(10)]

for qaseeda in qasaed:
    pprint(qaseeda)
    payload = ""
    for bait in qaseeda:
        payload += "\n".join(bait.split("#"))
        payload += "\n"
    print("*" * 80)
    print(payload)
    print("*" * 80)
    response = requests.post(
        "http://127.0.0.1:8000/api/analyze",
        data={"baits": payload},
    )
    time.sleep(5)
    if response.ok:
        pprint(response.json())
    break
