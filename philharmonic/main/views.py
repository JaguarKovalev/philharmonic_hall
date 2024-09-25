from django.http import JsonResponse
from django.shortcuts import render
from .models import (
    CulturalVenue,
    CulturalEvent,
    Artist,
    Impresario,
    Genre,
    ArtistGenre,
    Organizer,
    Contract,
    EventVenue,
    ArtistContract,
    ArtistEvent,
    CulturalVenueType,
    Person,
)


def get_venue_attributes(request, type_id):
    try:
        venue_type = CulturalVenueType.objects.get(id=type_id)
        return JsonResponse(
            {"default_attributes": {attr: None for attr in venue_type.attributes_list}}
        )
    except CulturalVenueType.DoesNotExist:
        return JsonResponse({"error": "Type not found"}, status=404)


def all_data_view(request):
    # Собираем данные из всех таблиц
    venues = CulturalVenue.objects.all()
    events = CulturalEvent.objects.all()
    artists = Artist.objects.all()
    impresarios = Impresario.objects.all()
    genres = Genre.objects.all()
    organizers = Organizer.objects.all()
    contracts = Contract.objects.all()
    event_venues = EventVenue.objects.all()
    artist_contracts = ArtistContract.objects.all()
    artist_events = ArtistEvent.objects.all()
    venue_types = CulturalVenueType.objects.all()
    people = Person.objects.all()
    artist_genres = ArtistGenre.objects.all()

    # Передаем данные в шаблон
    context = {
        "venues": venues,
        "events": events,
        "artists": artists,
        "impresarios": impresarios,
        "genres": genres,
        "organizers": organizers,
        "contracts": contracts,
        "event_venues": event_venues,
        "artist_contracts": artist_contracts,
        "artist_events": artist_events,
        "venue_types": venue_types,
        "people": people,
        "artist_genres": artist_genres,
    }
    return render(request, "main/all_data.html", context)
