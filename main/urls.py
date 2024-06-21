from django.urls import path
from . import views
from . import delete
from . import addBox
from . import addCar
from . import non

urlpatterns = [
    path('',non.non, name='non'),
    path('index/',views.index, name='index'),
    path('delete/',delete.delete, name='delete'),
    path('addBox/',addBox.addBox, name='addBox'),
    path('addCar/',addCar.addCar, name='addCar'),
]