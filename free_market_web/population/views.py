from django.shortcuts import render, redirect
from .forms import NewPopulationForm


def home_page(request):
    return render(request, 'home.html')


def new_universe(request):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            new_universe = form.save()
            redirect(new_universe)
        return render(request, 'new_universe.html', {'form': form})

    form = NewPopulationForm()
    return render(request, 'new_universe.html', {'form': form})
