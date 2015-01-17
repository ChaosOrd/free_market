from django.shortcuts import render
from .forms import NewPopulationForm


def home_page(request):
    return render(request, 'home.html')


def custom_population(request):
    if request.method == 'POST':
        form = NewPopulationForm(data=request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'custom_population.html', {'form': form})

    form = NewPopulationForm()
    return render(request, 'custom_population.html', {'form': form})
