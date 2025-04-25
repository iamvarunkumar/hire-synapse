"""
URL configuration for hire_synapse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
urlpatterns = [
    path('admin/', admin.site.urls),
    # Include authentication URLs (assuming from Sprint 1)
    # path('accounts/', include('django.contrib.auth.urls')), # Or your custom auth app
    # path('accounts/', include('your_auth_app.urls')),

    # Include profile URLs
    path('profile/', include('profiles.urls', namespace='profiles')),

    # Add other app URLs here
    # path('', include('core.urls')), # Example home page app
]
