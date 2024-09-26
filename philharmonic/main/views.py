from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection


from .forms import (
    ArtistGenreForm,
    ArtistImpresarioForm,
    EventFilterForm,
    VenueFilterForm,
    SQLQueryForm
)
from .models import (
    Artist,
    ArtistContract,
    ArtistEvent,
    ArtistGenre,
    Contract,
    CulturalEvent,
    CulturalVenue,
    CulturalVenueType,
    EventVenue,
    Genre,
    Impresario,
    Organizer,
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

def combined_view(request):
    # Формы
    venue_form = VenueFilterForm(request.GET or None)
    artist_genre_form = ArtistGenreForm(request.GET or None)
    artist_impresario_form = ArtistImpresarioForm(request.GET or None)
    event_form = EventFilterForm(request.GET or None)

    # Данные для культурных сооружений
    venues = CulturalVenue.objects.all()
    if venue_form.is_valid():
        venue_type = venue_form.cleaned_data.get('venue_type')
        min_capacity = venue_form.cleaned_data.get('min_capacity')
        if venue_type:
            venues = venues.filter(type=venue_type)
        if min_capacity:
            venues = venues.filter(specific_attributes__capacity__gte=min_capacity)

    # Данные для артистов по жанру
    artists_by_genre = Artist.objects.all()
    if artist_genre_form.is_valid():
        genre = artist_genre_form.cleaned_data.get('genre')
        if genre:
            artists_by_genre = artists_by_genre.filter(artist_genres__genre=genre)

    # Данные для артистов по импресарио
    artists_by_impresario = Artist.objects.all()
    if artist_impresario_form.is_valid():
        impresario = artist_impresario_form.cleaned_data.get('impresario')
        if impresario:
            artists_by_impresario = artists_by_impresario.filter(contracts__impresario=impresario)

    # Данные для мероприятий
    events = CulturalEvent.objects.all()
    if event_form.is_valid():
        start_date = event_form.cleaned_data.get('start_date')
        end_date = event_form.cleaned_data.get('end_date')
        organizer = event_form.cleaned_data.get('organizer')
        venue = event_form.cleaned_data.get('venue')
        if start_date and end_date:
            events = events.filter(eventvenue__event_date__range=[start_date, end_date])
        if organizer:
            events = events.filter(eventvenue__cultural_venue__events__organizer=organizer)
        if venue:
            events = events.filter(eventvenue__cultural_venue=venue)

    # Артисты в нескольких жанрах
    artists_in_multiple_genres = Artist.objects.annotate(genre_count=Count('artist_genres')).filter(genre_count__gt=1)

    # Отправляем все данные в шаблон
    context = {
        'venue_form': venue_form,
        'artist_genre_form': artist_genre_form,
        'artist_impresario_form': artist_impresario_form,
        'event_form': event_form,
        'venues': venues,
        'artists_by_genre': artists_by_genre,
        'artists_by_impresario': artists_by_impresario,
        'artists_in_multiple_genres': artists_in_multiple_genres,
        'events': events,
    }

    return render(request, 'main/combined_data.html', context)

def execute_sql_query(request):
    form = SQLQueryForm(request.POST or None)
    result = None
    error = None

    if form.is_valid():
        query = form.cleaned_data['query']
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                if query.lower().startswith('select'):
                    result = cursor.fetchall()  # Получаем данные, если запрос был SELECT
                else:
                    result = f"Запрос выполнен успешно. Затронуто {cursor.rowcount} строк."
        except Exception as e:
            error = str(e)

    return render(request, 'main/sql_query.html', {
        'form': form,
        'result': result,
        'error': error
    })