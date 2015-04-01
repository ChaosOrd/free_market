from django import forms
from django.forms.fields import TextInput
from population.models import Population, SupplyDemand, Universe

EMPTY_NAME_ERROR = 'Population name can not be empty'
EMPTY_QUANTITY_ERROR = 'Population quantity can not be empty'
INVALID_QUANTITY_ERROR = 'Population quantity is invalid'


class NewPopulationForm(forms.ModelForm):

    class Meta:
        model = Population
        fields = ('name', 'quantity',)

        labels = {
            'name': 'Population name', 'quantity': 'Quantity'
        }

        error_messages = {
            'name': {'required': EMPTY_NAME_ERROR},
            'quantity': {'required': EMPTY_QUANTITY_ERROR,
                         'invalid': INVALID_QUANTITY_ERROR},
        }

        widgets = {
            'name': TextInput(attrs={
                'tabindex': '1', 'title': 'Name',
            }),
            'quantity': TextInput(attrs={
                'tabindex': '2', 'title': 'Quantity',
            }),
        }

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(*args, data=data, **kwargs)

        self.sd_forms = []

        if data is not None:
            for sd_prefix in data.getlist('sd_prefix'):
                sd_form = SupplyDemandForm(prefix=sd_prefix, data=data)
                self.sd_forms.append(sd_form)

    def is_valid(self):
        main_form_valid = super().is_valid()
        sd_forms_valid = all(sd_form.is_valid() for sd_form in self.sd_forms)
        return main_form_valid and sd_forms_valid

    def save(self, for_universe):
        new_pop = Population.create_new(
            universe=for_universe, name=self.cleaned_data['name'],
            quantity=self.cleaned_data['quantity'])

        for sd_form in self.sd_forms:
            sd_form.save(for_population=new_pop)


INVALID_SD_VALUE_ERROR = 'Supply/Demand value is invalid'
EMPTY_SD_VALUE_ERROR = 'Supply/Demand value can not be empty'
EMPTY_RESOURCE_ERROR = 'Supply/Demand resource can not be empty'
TABINDEX_START = 2


class SupplyDemandForm(forms.ModelForm):

    def __init__(self, sd_num=None, *args, **kwargs):
        if sd_num is not None:
            kwargs['prefix'] = 'sd_{}'.format(sd_num)

        super().__init__(*args, **kwargs)

        if sd_num is not None:
            num_of_fields = len(self.fields)
            for idx, field_name in enumerate(self.fields):
                self.fields[field_name].widget.attrs['tabindex'] = \
                    str(TABINDEX_START + int(sd_num)*num_of_fields + idx)

    class Meta:
        model = SupplyDemand
        fields = ('resource', 'value',)
        error_messages = {
            'value': {
                'required': EMPTY_SD_VALUE_ERROR,
                'invalid': INVALID_SD_VALUE_ERROR,
            },
            'resource': {
                'required': EMPTY_RESOURCE_ERROR,
            },
        }
        widgets = {'value': TextInput()}

    def save(self, for_population):
        SupplyDemand.objects.create(population=for_population,
                                    resource=self.cleaned_data['resource'],
                                    value=self.cleaned_data['value'])


EMPTY_UNIVERSE_NAME_ERROR = 'Universe name can not be empty'


class UniverseForm(forms.ModelForm):

    class Meta:
        model = Universe
        fields = ('universe_name',)
        widgets = {
            'universe_name': TextInput(attrs={
                'tabindex': '0', 'title': 'Name',
            })
        },
        labels = {'universe_name': 'Universe name'}
        error_messages = {
            'universe_name': {
                'required': EMPTY_UNIVERSE_NAME_ERROR
            }
        }
