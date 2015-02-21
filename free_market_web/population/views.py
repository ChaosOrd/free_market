from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import NewPopulationForm, SupplyDemandForm
from population.models import Universe


def home_page(request):
    return render(request, 'home.html')


def supply_demand_form(request):
    form = SupplyDemandForm()
    return render(request, 'supply_demand_form.html', {'form': form})


class ExistingUniverseView(View):

    def get(self, request, universe_id):
        form = NewPopulationForm()
        return self._render_universe(request, universe_id, form)

    def post(self, request, universe_id):
        form = NewPopulationForm(data=request.POST)
        sd_forms = []
        sd_forms_valid = True

        if 'SupplyDemand' in request.POST:
            for sd_data in request.POST['SupplyDemand']:
                sd_form = SupplyDemandForm(data=request.POST)
                sd_forms_valid &= sd_form.is_valid()
                sd_forms.append(sd_form)
        if form.is_valid() and sd_forms_valid:
            return redirect(form.save(for_universe=universe_id,
                                      sd_forms=sd_forms))
        else:
            return self._render_universe(request, universe_id, form)

    def _render_universe(self, request, universe_id, form):
        universe = Universe.objects.get(id=universe_id)
        return render(request, 'universe.html', {'form': form,
                                                 'universe': universe})


class NewUniverseView(View):

    def get(self, request):
        form = NewPopulationForm()
        return render(request, 'new_universe.html', {'form': form})

    def post(self, request):
        form = NewPopulationForm(data=request.POST)
        sd_forms = []
        sd_forms_valid = True

        if 'SupplyDemand' in request.POST:
            for sd_data in request.POST['SupplyDemand']:
                sd_form = SupplyDemandForm(data=request.POST)
                sd_forms_valid &= sd_form.is_valid()
                sd_forms.append(sd_form)

        if form.is_valid() and sd_forms_valid:
            return redirect(form.save(sd_forms=sd_forms))
        else:
            return render(request, 'new_universe.html', {'form': form})
