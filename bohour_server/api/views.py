from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

# Create your views here.


class APIView(View):
    def process_bait(self, bait):
        """This method needs to be overridden"""
        return {"bait": bait}

    def get(self, request, *args, **kwrags):
        bait = request.GET.get("bait")
        result = self.process_bait(bait)
        return JsonResponse(data=result)
