from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html')


def custom_population(request):
    return render(request, 'custom_population.html')
