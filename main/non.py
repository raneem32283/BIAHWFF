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
def non(request):
    cities = City.objects.all()
    boxes = Box.objects.all()
    cars = Car.objects.all()
    return render(request, 'pages/index.html', {'cities': cities, 'boxes': boxes, 'cars': cars
                                                    })   