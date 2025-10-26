from django.urls import path

from data_visualization import views

urlpatterns = [
    path('', views.index, name='index'),

]
