"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from her.views import register_view, login_view
from django.contrib.auth import logout


def user_logout(request):
    logout(request)
    return redirect('/my/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/my/', permanent=False), name='dashboard'),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('my/', include('her.urls', namespace="her")),
    path("settings/", include("edit.urls", namespace="edit")),
    path('logout/', user_logout, name="logout")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)