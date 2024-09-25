from django.urls import path
from .views import get_venue_attributes
from .views import all_data_view

urlpatterns = [
    path(
        "get_venue_attributes/<int:type_id>/",
        get_venue_attributes,
        name="get_venue_attributes",
    ),
    path("all-data/", all_data_view, name="all_data"),
]
