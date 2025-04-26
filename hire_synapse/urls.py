from django.contrib import admin
from django.urls import path, include # Make sure 'include' is imported and this line has NO leading whitespace
# Remove RedirectView imports if they were added before
# from django.views.generic.base import RedirectView
# from django.urls import reverse_lazy

urlpatterns = [
    # Map the root path ('') to the urls defined in the 'core' app
    path('', include('core.urls', namespace='core')), # Ensure this line is correctly indented

    # Admin site URL
    path('admin/', admin.site.urls), # Ensure this line is correctly indented

    # Include URLs from your other apps
    path('profile/', include('profiles.urls', namespace='profiles')), # Ensure this line is correctly indented
    path('documents/', include('documents.urls', namespace='documents')), # Ensure this line is correctly indented
    path('jobs/', include('jobs.urls', namespace='jobs')), # Ensure this line is correctly indented

    # Add include for authentication URLs if you have them
    # path('accounts/', include('django.contrib.auth.urls')), # Ensure this line is correctly indented
]