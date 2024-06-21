from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from collections import defaultdict
import random
import numpy as np
from .models import City
from .models import Box
from .models import Car

def addCar(request):
    weight_of_trak=0
    capacity=0
    if request.method == 'POST':
        if 'weight_of_trak' in request.POST:
            weight_of_trak = request.POST.get('weight_of_trak')
            capacity = request.POST.get('weight_of_trak')
            Car(weight_of_trak=weight_of_trak,capacity=capacity).save(True)
        cities = City.objects.all()
        boxes = Box.objects.all()
        cars = Car.objects.all()
        return render(request, 'pages/index.html', {'cities': cities, 'boxes': boxes, 'cars': cars})