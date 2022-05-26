from api.views import BaitDiacritizerAPIView


from django.urls import path

urlpatterns = [
    path(
        "diacritize",
        BaitDiacritizerAPIView.as_view(),
        name="bait_diacritizer",
    ),
]
