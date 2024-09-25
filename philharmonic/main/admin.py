from django.contrib import admin
from .models import (
    Person,
    Artist,
    Genre,
    ArtistGenre,
    Impresario,
    Organizer,
    Contract,
    CulturalEvent,
    CulturalVenue,
    CulturalVenueType,
    EventVenue,
    ArtistContract,
    ArtistEvent,
)
from .forms import CulturalVenueForm


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "middle_name", "email")


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "is_national_artist",
        "foreign_language",
        "favorite_musical_instrument",
    )
    search_fields = ("person__last_name", "person__first_name")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "main_instrument")


@admin.register(ArtistGenre)
class ArtistGenreAdmin(admin.ModelAdmin):
    list_display = ("artist", "genre", "experience")


@admin.register(Impresario)
class ImpresarioAdmin(admin.ModelAdmin):
    list_display = ("person", "rating", "experience")


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("person", "is_logistics_specialist", "role")


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("contract_date", "impresario", "organizer")


@admin.register(CulturalEvent)
class CulturalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "event_type", "tickets_sold")


@admin.register(CulturalVenueType)
class CulturalVenueTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name",)


@admin.register(CulturalVenue)
class CulturalVenueAdmin(admin.ModelAdmin):
    form = CulturalVenueForm

    class Media:
        js = ("main/venue_form.js",)

    list_display = ("name", "address", "type")


@admin.register(EventVenue)
class EventVenueAdmin(admin.ModelAdmin):
    list_display = ("cultural_event", "cultural_venue", "event_date")


@admin.register(ArtistContract)
class ArtistContractAdmin(admin.ModelAdmin):
    list_display = ("artist", "impresario", "contract_date", "contract_duration")


@admin.register(ArtistEvent)
class ArtistEventAdmin(admin.ModelAdmin):
    list_display = ("artist", "cultural_event", "is_winner", "is_prize_winner")
