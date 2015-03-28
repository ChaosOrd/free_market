from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import NewPopulationForm, SupplyDemandForm, UniverseForm
from population.models import Population, Universe


def home_page(request):
    return render(request, 'home.html')


def supply_demand_form(request, next_sd_num):
    form = SupplyDemandForm(sd_num=int(next_sd_num))
    return render(request, 'supply_demand_form.html', {'form': form})


def delete_population(request, population_id):
    population = Population.objects.get(id=population_id)
    universe = population.universe
    population.delete()
    return redirect(universe)


class BaseUniverseView(View):

    def get(self, request, universe_id=None):
        form = NewPopulationForm()
        return self._render_universe(request, universe_id, form)

    def post(self, request, universe_id=None):
        universe_form = UniverseForm(data=request.POST)
        pop_form = NewPopulationForm(data=request.POST)

        if universe_form.is_valid() and pop_form.is_valid():
            universe_form.save()
            return redirect(pop_form.save(for_universe=universe_id))
        else:
            return self._render_universe(request, universe_id, pop_form)

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
