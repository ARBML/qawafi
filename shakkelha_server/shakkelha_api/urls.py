from django.urls import path
from .views import BaitDiacritizerAPIView

urlpatterns = [
    path(
        "diacritize",
        BaitDiacritizerAPIView.as_view(),
        name="bait_diacritization_view",
    )
]
