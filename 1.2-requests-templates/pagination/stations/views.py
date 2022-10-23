import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open(settings.BUS_STATION_CSV) as csvfile:
        page_number = int(request.GET.get('page', 1))
        reader = csv.DictReader(csvfile, dialect='unix')
        stations = [row for row in reader]
        paginator = Paginator(stations, 10)
        page_stations = paginator.get_page(page_number)
        context = {
            'bus_stations': page_stations,
            'page': page_stations,
        }
        return render(request, 'stations/index.html', context)
