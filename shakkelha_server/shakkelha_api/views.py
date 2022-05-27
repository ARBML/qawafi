import os
import json
import tnkeeh as tn
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


class APIView(View):
    def process_bait(self, bait):
        """This method needs to be overridden"""
        return {"bait": bait}

    def get(self, request, *args, **kwrags):
        bait = request.GET.get("bait")
        result = self.process_bait(bait)
        return JsonResponse(data=result)


@method_decorator(csrf_exempt, name="dispatch")
class BaitDiacritizerAPIView(View):
    def diacritize(self, baits):
        with open("./baits_input.txt", "w") as baits_file:
            baits_file.write("\n".join(baits))
        tn.clean_data(
            file_path="./baits_input.txt",
            save_path="./baits_input.txt",
            remove_diacritics=True,
            # remove_special_chars=True,
            remove_tatweel=True,
        )
        # diacritize
        os.system("bash diacritization_command.bash")
        diacritized_baits = open("./baits_output.txt").read().splitlines()
        return diacritized_baits

    def post(self, request, *args, **kwargs):
        baits = json.loads(request.POST.get("baits"))
        diacritized_baits = self.diacritize(baits)
        return JsonResponse(
            {"diacritized": diacritized_baits},
            json_dumps_params={"ensure_ascii": False},
        )
