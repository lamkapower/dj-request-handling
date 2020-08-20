from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
import csv

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, 'r', encoding='cp1251') as f:
        data = []
        page = request.GET.get('page')
        prev_page_url = None
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
        paginator = Paginator(data, 10)
        page_obj = paginator.get_page(page)
        if page_obj.has_next():
            next_page_url = page_obj.next_page_number()
        if page_obj.has_previous():
            prev_page_url = page_obj.previous_page_number()
        return render_to_response('index.html', context={
            'bus_stations': page_obj,
            'current_page': page_obj.number,
            'prev_page_url': prev_page_url,
            'next_page_url': next_page_url,
        })

