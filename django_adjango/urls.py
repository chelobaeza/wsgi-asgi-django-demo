"""
URL configuration for django_adjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from async_app import views as async_views
from sync_app import views as sync_views

urlpatterns = [
    path("sync/blocking/", sync_views.blocking),
    path("sync/comp/<int:times>/", sync_views.computation),

    path("async/non-blocking/", async_views.non_blocking),
    path("async/blocking/", async_views.blocking),
    path("async/comp/<int:times>/", async_views.computation),
]
