from django.urls import path
from . import views 

app_name = "edit"

urlpatterns = [
    path("new/", views.new, name="new")
]
