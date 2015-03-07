from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import NewPopulationForm, SupplyDemandForm
from population.models import Universe


def home_page(request):
    return render(request, 'home.html')


def supply_demand_form(request, next_sd_num):
    form = SupplyDemandForm(sd_num=int(next_sd_num))
    return render(request, 'supply_demand_form.html', {'form': form})


class BaseUniverseView(View):

    def get(self, request, universe_id=None):
        form = NewPopulationForm()
        return self._render_universe(request, universe_id, form)

    def post(self, request, universe_id=None):
        form = NewPopulationForm(data=request.POST)
        sd_forms = self._create_supply_demand_forms_from_request(request)
        sd_forms_valid = all(sd_form.is_valid() for sd_form in sd_forms)

        if form.is_valid() and sd_forms_valid:
            return redirect(form.save(for_universe=universe_id,
                                      sd_forms=sd_forms))
        else:
            return self._render_universe(request, universe_id, form)

    def _create_supply_demand_forms_from_request(self, request):
        sd_forms = []

        if 'sd_prefix' in request.POST:
            for sd_prefix in request.POST.getlist('sd_prefix'):
                sd_form = SupplyDemandForm(data=request.POST,
                                           prefix=sd_prefix)
                sd_forms.append(sd_form)

        return sd_forms

    def _render_universe(self, request, universe_id, form):
        render_data = {'form': form}

        if universe_id is not None:
            render_data['universe'] = Universe.objects.get(id=universe_id)

        return render(request, self.template_name, render_data)

    @property
    def template_name(self):
        return None


class ExistingUniverseView(BaseUniverseView):

    @property
    def template_name(self):
        return 'universe.html'


class NewUniverseView(BaseUniverseView):

    @property
    def template_name(self):
        return 'new_universe.html'
