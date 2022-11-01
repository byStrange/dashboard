from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from her.views import register_view, login_view, render
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