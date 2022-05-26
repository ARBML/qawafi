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
    response = requests.post(
        "http://127.0.0.1:8000/api/analyze",
        data={"baits": json.dumps(qaseeda, ensure_ascii=False)},
    )
    time.sleep(5)
    if response.ok:
        pprint(response.json())
