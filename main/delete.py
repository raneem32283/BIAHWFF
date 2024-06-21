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

def delete(request):
    myCar=Car.objects.all()
    myCar.delete()
    myBox=Box.objects.all()
    myBox.delete()
    return render(request, 'pages/index.html', {'cities': '', 'boxes': '', 'cars': ''})