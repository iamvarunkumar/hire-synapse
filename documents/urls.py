from django.urls import path
from . import views # Import views from the current directory (documents app)

# Define the app namespace. This is important for reversing URLs.
# Example: {% url 'documents:coverletter_list' %} in templates
app_name = 'documents'

# Define the URL patterns for the documents app
urlpatterns = [
    # URL for listing all cover letters (maps to CoverLetterListView)
    # Example URL: /cover-letters/
    path('', views.CoverLetterListView.as_view(), name='coverletter_list'),

    # URL for creating a new cover letter (maps to CoverLetterCreateView)
    # Example URL: /cover-letters/create/
    path('create/', views.CoverLetterCreateView.as_view(), name='coverletter_create'),

    # URL for editing an existing cover letter (maps to CoverLetterUpdateView)
    # <int:pk> captures the primary key (ID) of the cover letter from the URL
    # Example URL: /cover-letters/5/edit/
    path('<int:pk>/edit/', views.CoverLetterUpdateView.as_view(), name='coverletter_edit'),

    # URL for deleting an existing cover letter (maps to CoverLetterDeleteView)
    # Example URL: /cover-letters/5/delete/
    path('<int:pk>/delete/', views.CoverLetterDeleteView.as_view(), name='coverletter_delete'),

    # Optional detail view URL (if you create a CoverLetterDetailView)
    # path('<int:pk>/', views.CoverLetterDetailView.as_view(), name='coverletter_detail'),
]