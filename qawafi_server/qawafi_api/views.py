import json

import requests

from bohour.arudi_style import get_arudi_style
from bohour.qafiah import get_qafiah_type, get_qafiyah
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from collections import Counter
from difflib import SequenceMatcher
from django.conf import settings
from pyarabic.araby import strip_tashkeel

from qawafi_server.utils import clean

# Create your views here.

majority_vote = lambda a: Counter(a).most_common()[0][0]


@method_decorator(csrf_exempt, name="dispatch")
class BaitAnalyzerAPIView(View):
    def diacritize(self, baits):
        response = requests.post(
            f"{settings.DIACRITIZER_HOST_URL}/api/diacritize",
            data={"baits": json.dumps(baits, ensure_ascii=False)},
        )
        if response.ok:
            return response.json()
        return None

    def process_baits_string(self, input):
        lines = input.strip().split("\n")
        baits = []
        for i in range(len(lines) // 2):
            bait = " # ".join(lines[i * 2 : (i + 1) * 2])
            bait = clean(bait)
            baits.append(bait)
        return baits

    def post(self, request, *args, **kwargs):
        baits = self.process_baits_string(request.POST.get("baits"))
        analyzer = settings.BAITS_ANALYZER
        # baits = [baits[0]]
        # diacritized_baits = self.diacritize(baits)["diacritized"]
        analysis = analyzer.analyze(
            baits=baits,
            diacritized_baits=None,
            return_closest_baits=False,
            short_qafiyah=True,
            override_tashkeel=True,
        )
        return JsonResponse(
            analysis,
            json_dumps_params={"ensure_ascii": False},
        )
