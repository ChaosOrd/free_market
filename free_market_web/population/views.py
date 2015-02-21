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
        if form.is_valid():
            if 'SupplyDemand' in request.POST:
                sp_forms = []
                for sp_data in request.POST['SupplyDemand']:
                    sp_forms.append(SupplyDemandForm(data=request.POST))

            return redirect(form.save(for_universe=universe_id))
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
        if form.is_valid():
            return redirect(form.save())
        else:
            return render(request, 'new_universe.html', {'form': form})

