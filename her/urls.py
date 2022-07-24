from django.urls import path
from . import views

app_name = "her"

urlpatterns = [
    path('', views.welcome, name="index"),
    path('test/', views.testview, name="test"),
]
