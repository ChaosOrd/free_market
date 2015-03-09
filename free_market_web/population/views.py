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

        if form.is_valid():
            return redirect(form.save(for_universe=universe_id))
        else:
            return self._render_universe(request, universe_id, form)

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
