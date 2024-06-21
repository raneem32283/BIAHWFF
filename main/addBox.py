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

def addBox(request):
    weight=0
    value=0
    destination_id=0
    if request.method == 'POST':
        if 'weight' in request.POST and 'value' in request.POST:
            weight = request.POST.get('weight')
            value = request.POST.get('value')
            destination_id = request.POST.get('destination')
            Box(weight=weight,value=value,destination_id=destination_id).save(False)
        cities = City.objects.all()
        boxes = Box.objects.all()
        cars = Car.objects.all()
        return render(request, 'pages/index.html', {'cities': cities, 'boxes': boxes, 'cars': cars})