from django.http import JsonResponse
from .models import CulturalVenueType


def get_venue_attributes(request, type_id):
    try:
        venue_type = CulturalVenueType.objects.get(id=type_id)
        return JsonResponse(
            {"default_attributes": {attr: None for attr in venue_type.attributes_list}}
        )
    except CulturalVenueType.DoesNotExist:
        return JsonResponse({"error": "Type not found"}, status=404)
