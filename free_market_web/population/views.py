from django.shortcuts import render, redirect
from .forms import NewPopulationForm, SupplyDemandForm
from population.models import Universe


def home_page(request):
    return render(request, 'home.html')


def new_universe(request):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            return redirect(form.save())
    else:
        form = NewPopulationForm()

    return render(request, 'new_universe.html', {'form': form})


def universe(request, universe_id):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            return redirect(form.save(for_universe=universe_id))
    else:
        form = NewPopulationForm()

    universe = Universe.objects.get(id=universe_id)
    return render(request, 'universe.html', {'form': form,
                                             'universe': universe})


def supply_demand_form(request):
    form = SupplyDemandForm()
    return render(request, 'supply_demand_form.html', {'form': form})
