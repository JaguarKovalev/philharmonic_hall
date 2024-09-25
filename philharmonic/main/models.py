from django.db import models


# General person model
class Person(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Artist model
class Artist(models.Model):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="artist"
    )
    is_national_artist = models.BooleanField(default=False)
    foreign_language = models.CharField(max_length=255, blank=True, null=True)
    favorite_musical_instrument = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        return f"Artist: {self.person}"


# Genre model
class Genre(models.Model):
    name = models.CharField(max_length=255)
    main_instrument = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


# Relationship between artist and genre
class ArtistGenre(models.Model):
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="artist_genres"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="artist_genres"
    )
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.artist} in {self.genre}"


# Impresario model
class Impresario(models.Model):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="impresario"
    )
    rating = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Impresario: {self.person}"


# Organizer model
class Organizer(models.Model):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, related_name="organizer"
    )
    is_logistics_specialist = models.BooleanField(default=False)
    role = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Organizer: {self.person}"


# Contract between impresario and organizer
class Contract(models.Model):
    contract_date = models.DateField()
    impresario = models.ForeignKey(
        Impresario, on_delete=models.CASCADE, related_name="contracts"
    )
    organizer = models.ForeignKey(
        Organizer, on_delete=models.CASCADE, related_name="contracts"
    )

    def __str__(self):
        return f"Contract on {self.contract_date} between {self.impresario} and {self.organizer}"


# Cultural event model
class CulturalEvent(models.Model):
    EVENT_TYPES = [
        ("concert", "Concert"),
        ("competition", "Competition"),
        ("exhibition", "Exhibition"),
    ]
    event_type = models.CharField(max_length=255, choices=EVENT_TYPES)
    tickets_sold = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Model for types of cultural venues
class CulturalVenueType(models.Model):
    type_name = models.CharField(
        max_length=100, unique=True
    )  # Название типа (театр, кинотеатр и т.д.)
    attributes_list = models.JSONField(default=list)  # Список атрибутов (без значений)

    def __str__(self):
        return self.type_name


class CulturalVenue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.ForeignKey(CulturalVenueType, on_delete=models.CASCADE)
    specific_attributes = models.JSONField(
        default=dict
    )  # JSONField для хранения атрибутов

    def save(self, *args, **kwargs):
        # Если атрибуты не заданы, подставляем их с нулевыми значениями на основе типа
        if not self.specific_attributes:
            default_attributes = {attr: None for attr in self.type.attributes_list}
            self.specific_attributes = default_attributes
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Relationship between events and venues
class EventVenue(models.Model):
    event_date = models.DateField()
    cultural_venue = models.ForeignKey(
        CulturalVenue, on_delete=models.CASCADE, related_name="events"
    )
    cultural_event = models.ForeignKey(
        CulturalEvent, on_delete=models.CASCADE, related_name="venues"
    )

    def __str__(self):
        return f"{self.cultural_event} at {self.cultural_venue} on {self.event_date}"


# Contract between artist and impresario
class ArtistContract(models.Model):
    contract_date = models.DateField()
    contract_duration = models.PositiveIntegerField()
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="contracts"
    )
    impresario = models.ForeignKey(
        Impresario, on_delete=models.CASCADE, related_name="artist_contracts"
    )

    def __str__(self):
        return (
            f"Contract with {self.artist} and {self.impresario} on {self.contract_date}"
        )


# Relationship between artists and events
class ArtistEvent(models.Model):
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="artist_events"
    )
    cultural_event = models.ForeignKey(
        CulturalEvent, on_delete=models.CASCADE, related_name="artist_events"
    )
    is_winner = models.BooleanField(default=False)
    is_prize_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.artist} at {self.cultural_event}"
