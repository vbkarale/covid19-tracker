from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('country/<str:cname>', views.country, name='country'),
    path('demo/', views.demo, name='demo')
]
