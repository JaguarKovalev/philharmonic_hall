from django.urls import path
from .views import get_venue_attributes

urlpatterns = [
    path(
        "get_venue_attributes/<int:type_id>/",
        get_venue_attributes,
        name="get_venue_attributes",
    ),
]
