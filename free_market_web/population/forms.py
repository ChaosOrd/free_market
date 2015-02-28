from django import forms
from django.forms import ModelChoiceField, HiddenInput
from population.models import Population, Resource, SupplyDemand, Universe

EMPTY_NAME_ERROR = 'Population name can not be empty'
EMPTY_QUANTITY_ERROR = 'Population quantity can not be empty'
INVALID_QUANTITY_ERROR = 'Population quantity is invalid'


class NewPopulationForm(forms.ModelForm):

    class Meta:
        model = Population
        fields = ('name', 'quantity',)

        labels = {
            'name': 'Name', 'quantity': 'Quantity'
        }

        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR},
            'quantity': {'required': EMPTY_QUANTITY_ERROR,
                         'invalid': INVALID_QUANTITY_ERROR},
        }

        widgets = {
            'name': forms.fields.TextInput(attrs={
                'tabindex': '0', 'title': 'Name',
            }),
            'quantity': forms.fields.TextInput(attrs={
                'tabindex': '1', 'title': 'Quantity',
            }),
        }

    def save(self, sd_forms, for_universe=None):
        if for_universe is None:
            universe = Universe.create_new()
        else:
            universe = Universe.objects.get(id=for_universe)

        new_pop = Population.create_new(
            universe=universe, name=self.cleaned_data['name'],
            quantity=self.cleaned_data['quantity'])

        for sd_form in sd_forms:
            sd_form.save(for_population=new_pop)

        return universe


INVALID_SD_VALUE_ERROR = 'Supply/Demand value is invalid'
EMPTY_SD_VALUE_ERROR = 'Supply/Demand value can not be empty'
EMPTY_RESOURCE_ERROR = 'Resource can not be empty'


class SupplyDemandForm(forms.ModelForm):

    resource = ModelChoiceField(queryset=Resource.objects.all(),
                                error_messages={
                                    'required': EMPTY_RESOURCE_ERROR,
                                })

    class Meta:
        model = SupplyDemand
        fields = ('resource', 'value',)
        error_messages = {
            'value': {
                'required': EMPTY_SD_VALUE_ERROR,
                'invalid': INVALID_SD_VALUE_ERROR
            },
        }

    def save(self, for_population):
        SupplyDemand.objects.create(population=for_population,
                                    resource=self.cleaned_data['resource'],
                                    value=self.cleaned_data['value'])
