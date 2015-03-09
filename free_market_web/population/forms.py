from django import forms
from django.forms import ModelChoiceField
from django.forms.fields import Select, TextInput
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
            'name': TextInput(attrs={
                'tabindex': '0', 'title': 'Name',
            }),
            'quantity': TextInput(attrs={
                'tabindex': '1', 'title': 'Quantity',
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
        sd_forms_valid = all(sd_form.is_valid() for sd_form in self.sd_forms)
        return sd_forms_valid and super().is_valid()

    def save(self, for_universe=None):
        if for_universe is None:
            universe = Universe.create_new()
        else:
            universe = Universe.objects.get(id=for_universe)

        new_pop = Population.create_new(
            universe=universe, name=self.cleaned_data['name'],
            quantity=self.cleaned_data['quantity'])

        for sd_form in self.sd_forms:
            sd_form.save(for_population=new_pop)

        return universe


INVALID_SD_VALUE_ERROR = 'Supply/Demand value is invalid'
EMPTY_SD_VALUE_ERROR = 'Supply/Demand value can not be empty'
EMPTY_RESOURCE_ERROR = 'Supply/Demand resource can not be empty'
TABINDEX_START = 2


class SupplyDemandForm(forms.ModelForm):

    resource = ModelChoiceField(queryset=Resource.objects.all(),
                                error_messages={'required':
                                                EMPTY_RESOURCE_ERROR, })

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
                'invalid': INVALID_SD_VALUE_ERROR
            },
        }

    def save(self, for_population):
        SupplyDemand.objects.create(population=for_population,
                                    resource=self.cleaned_data['resource'],
                                    value=self.cleaned_data['value'])
