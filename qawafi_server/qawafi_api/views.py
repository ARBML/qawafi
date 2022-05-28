import json

import requests

from bohour.arudi_style import get_arudi_style
from bohour.qafiah import get_qafiah_type, get_qafiyah
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from qawafi_server.meters import (
    get_closest_baits,
    get_meter,
    predict_era,
    predict_theme,
)
from collections import Counter
from difflib import SequenceMatcher
from django.conf import settings
from pyarabic.araby import strip_tashkeel

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

    def similarity_score(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def check_similarity(self, tf3, bahr):
        out = []
        meter = settings.BOHOUR_NAMES[settings.BOHOUR_NAMES_AR.index(bahr)]
        for comb, tafeelat in zip(
            settings.BOHOUR_PATTERNS[meter],
            settings.BOHOUR_TAFEELAT[meter],
        ):
            prob = self.similarity_score(tf3, comb)
            out.append((comb, prob, tafeelat))
        return sorted(out, key=lambda x: x[1], reverse=True)

    def get_closest_patterns(self, patterns, meter):
        most_similar_patterns = list()
        for pattern in patterns:
            most_similar_patterns.append(
                self.check_similarity(
                    tf3=pattern,
                    bahr=meter,
                )[0]
            )
        return most_similar_patterns

    def post(self, request, *args, **kwargs):
        baits = json.loads(request.POST.get("baits"))
        baits = [baits[0]]
        diacritized_baits = self.diacritize(baits)["diacritized"]
        arudi_styles_and_patterns = get_arudi_style(diacritized_baits)
        meter = majority_vote(get_meter(baits))
        most_closest_patterns = self.get_closest_patterns(
            patterns=[pattern for (arudiy_style, pattern) in arudi_styles_and_patterns],
            meter=meter,
        )
        qafiyah = majority_vote(get_qafiyah(baits))
        # meters = get_meter(diacritized_baits)
        # res = get_closest_baits(baits)
        era = predict_era(strip_tashkeel(" ".join(baits)))
        theme = predict_theme(strip_tashkeel(" ".join(baits)))
        return JsonResponse(
            {
                "diacritized": diacritized_baits,
                "arudi_style": arudi_styles_and_patterns,
                "qafiyah": qafiyah,
                "meter": meter,
                # "closest_baits": res,
                "era": era,
                "closest_patterns": most_closest_patterns,
                "theme": theme,
            },
            json_dumps_params={"ensure_ascii": False},
        )
