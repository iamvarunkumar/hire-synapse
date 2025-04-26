from django.urls import path
from .views import HomePageView # Import the view

app_name = 'core' # Define app namespace <--- ADD THIS LINE

urlpatterns = [
    # Map the empty path within this app to the HomePageView
    path('', HomePageView.as_view(), name='home'),
]
