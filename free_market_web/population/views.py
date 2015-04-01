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
        return self._render_universe(request, universe_id)

    def post(self, request, universe_id=None):
        universe_form = UniverseForm(data=request.POST)
        pop_form = NewPopulationForm(data=request.POST)

        if universe_form.is_valid() and pop_form.is_valid():
            universe = self._save_universe(universe_form, universe_id)
            pop_form.save(for_universe=universe)
            return redirect(universe)
        else:
            return self._render_universe(request, universe_id)

    def _save_universe(self, universe_form, universe_id):
        if universe_id is not None:
            universe = Universe.objects.get(id=universe_id)
            return universe_form.save(instance=universe)
        else:
            return universe_form.save()

    def _render_universe(self, request, universe_id):
        if universe_id is not None:
            render_data = self._get_existing_universe_render_data(universe_id)
        else:
            render_data = self._get_new_universe_render_data()

        return render(request, self.template_name, render_data)

    def _get_new_universe_render_data(self):
        pop_form = NewPopulationForm()
        universe_form = UniverseForm()

        return {'pop_form': pop_form, 'universe_form': universe_form}

    def _get_existing_universe_render_data(self, universe_id):
        universe =  Universe.objects.get(id=universe_id)

        pop_form = NewPopulationForm()
        universe_form = UniverseForm(instance=universe)

        return {'pop_form': pop_form, 'universe_form': universe_form,
                'universe': universe}

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
