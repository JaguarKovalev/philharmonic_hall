from django import forms
from .models import CulturalVenueType, Genre, Impresario, Organizer, CulturalVenue


class CulturalVenueForm(forms.ModelForm):
    class Meta:
        model = CulturalVenue
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CulturalVenueForm, self).__init__(*args, **kwargs)
        # Проверяем, что экземпляр существует и что у него есть тип
        if self.instance.pk and self.instance.type:
            attributes_list = self.instance.type.attributes_list
            self.fields['specific_attributes'].help_text = f"Required attributes: {', '.join(attributes_list)}"

class VenueFilterForm(forms.Form):
    venue_type = forms.ModelChoiceField(
        queryset=CulturalVenueType.objects.all(), 
        required=False, 
        label="Тип культурного сооружения"
    )
    min_capacity = forms.IntegerField(required=False, label="Минимальная вместимость")

class ArtistGenreForm(forms.Form):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label="Жанр")

class ArtistImpresarioForm(forms.Form):
    impresario = forms.ModelChoiceField(queryset=Impresario.objects.all(), label="Импресарио")

class EventFilterForm(forms.Form):
    start_date = forms.DateField(required=True, label="Дата начала")
    end_date = forms.DateField(required=True, label="Дата окончания")
    organizer = forms.ModelChoiceField(queryset=Organizer.objects.all(), required=False, label="Организатор")
    venue = forms.ModelChoiceField(queryset=CulturalVenue.objects.all(), required=False, label="Культурное сооружение")