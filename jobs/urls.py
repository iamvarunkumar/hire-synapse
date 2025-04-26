from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListSearchView.as_view(), name='job_list_search'),
]