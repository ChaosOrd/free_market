from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
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


@login_required
def my_universes_view(request):
    my_universes = Universe.objects.filter(owner=request.user)
    return render(request, 'my_universes.html', {'my_universes': my_universes})


class BaseUniverseView(View):

    def save_forms_data(self, request):
        if self.universe_form.is_valid() and self.pop_form.is_valid():
            universe = self.universe_form.save(commit=False)
            universe.owner = request.user
            universe.save()
            self.pop_form.save(for_universe=universe)
            return redirect(universe)
        else:
            return self._render_forms(request)

    def _render_forms(self, request):
        return render(request, self.template_name,
                      {'pop_form': self.pop_form,
                       'universe_form': self.universe_form})

    @property
    def template_name(self):
        return None


class ExistingUniverseView(BaseUniverseView):

    @property
    def template_name(self):
        return 'universe.html'

    def get(self, request, universe_id):
        universe = Universe.objects.get(id=universe_id)

        if universe.owner != request.user:
            raise PermissionDenied()

        self.pop_form = NewPopulationForm()
        self.universe_form = UniverseForm(instance=universe)
        return self._render_forms(request)

    def post(self, request, universe_id):
        universe = Universe.objects.get(id=universe_id)

        if request.user != universe.owner:
            raise PermissionDenied()

        self.pop_form = NewPopulationForm(data=request.POST)
        self.universe_form = UniverseForm(data=request.POST,
                                          instance=universe)
        return self.save_forms_data(request)


class NewUniverseView(BaseUniverseView):

    @property
    def template_name(self):
        return 'new_universe.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        self.pop_form = NewPopulationForm()
        self.universe_form = UniverseForm()
        return self._render_forms(request)

    def post(self, request):
        self.pop_form = NewPopulationForm(data=request.POST)
        self.universe_form = UniverseForm(data=request.POST)
        return self.save_forms_data(request)
