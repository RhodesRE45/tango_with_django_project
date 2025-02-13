from django.urls import path
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<str:category_name>/', views.show_category, name='show_category'),
]
