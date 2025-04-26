# interviews/urls.py

from django.urls import path
from . import views # Import views from the current app

app_name = 'interviews' # Define the namespace for this app's URLs

urlpatterns = [
    # Map the root URL of this app ('/interview-prep/') to the InterviewQuestionListView
    path('', views.InterviewQuestionListView.as_view(), name='question_list'),
]
