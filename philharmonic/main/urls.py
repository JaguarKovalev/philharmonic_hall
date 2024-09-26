from django.urls import path

from .views import (
    get_venue_attributes,
    all_data_view,
    combined_view,
    execute_sql_query
)

urlpatterns = [
    path(
        "get_venue_attributes/<int:type_id>/",
        get_venue_attributes,
        name="get_venue_attributes",
    ),
    path("all-data/", all_data_view, name="all_data"),
    path('combined-data/', combined_view, name='combined_data'),
    path('sql-query/', execute_sql_query, name='sql_query'),
]
