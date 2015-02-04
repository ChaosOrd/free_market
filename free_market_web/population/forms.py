from django import forms
from population.models import Population, Universe

EMPTY_NAME_ERROR = 'Population name can not be empty'
EMPTY_QUANTITY_ERROR = 'Population quantity can not be empty'
INVALID_QUANTITY_ERROR = 'Population quantity is invalid'


class NewPopulationForm(forms.ModelForm):

    class Meta:
        model = Population
        fields = ('name', 'quantity',)

        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR},
            'quantity': {'required': EMPTY_QUANTITY_ERROR,
                         'invalid': INVALID_QUANTITY_ERROR},
        }

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'tabindex': '0',
            }),
            'quantity': forms.fields.TextInput(attrs={
                'tabindex': '1',
            }),
        }

    def save(self, for_universe=None):
        if for_universe is None:
            universe = Universe.create_new()
        else:
            universe = Universe.objects.get(id=for_universe)

        Population.create_new(universe=universe,
                              name=self.cleaned_data['name'],
                              quantity=self.cleaned_data['quantity'])
        return universe

class ResourceForm(forms.ModelForm):
    pass
