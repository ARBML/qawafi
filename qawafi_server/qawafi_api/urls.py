from qawafi_api.views import BaitAnalyzerAPIView


from django.urls import path

urlpatterns = [
    path(
        "analyze",
        BaitAnalyzerAPIView.as_view(),
        name="bait_analyzer",
    ),
]
