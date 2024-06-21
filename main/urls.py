from django.urls import path
from . import views
urlpatterns = [

    path('',views.index, name='index'),
    # path('',views.run_algorithms, name='run_algorithms'),
    # path('',views.your_view, name='your_view'),
    # path('',views.your_endpoint, name='your_endpoint'),
]