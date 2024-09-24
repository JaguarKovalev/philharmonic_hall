from django import forms
from .models import CulturalVenue

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
