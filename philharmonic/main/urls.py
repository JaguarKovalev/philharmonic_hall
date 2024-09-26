from django.urls import path
from .views import get_venue_attributes
from .views import all_data_view
from .views import combined_view

urlpatterns = [
    path(
        "get_venue_attributes/<int:type_id>/",
        get_venue_attributes,
        name="get_venue_attributes",
    ),
    path("all-data/", all_data_view, name="all_data"),
    path('combined-data/', combined_view, name='combined_data'),
]
