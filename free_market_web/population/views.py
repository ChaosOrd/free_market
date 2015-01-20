from django.shortcuts import render, redirect
from .forms import NewPopulationForm
from population.models import Universe


def home_page(request):
    return render(request, 'home.html')


def new_universe(request):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            return redirect(form.save())

    form = NewPopulationForm()
    return render(request, 'new_universe.html', {'form': form})


def universe(request, universe_id):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            return redirect(form.save(for_universe=universe_id))

    form = NewPopulationForm()
    universe = Universe.objects.get(id=universe_id)
    return render(request, 'universe.html', {'form': form,
                                             'universe': universe})
