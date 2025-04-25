from django.urls import path
from . import views

app_name = 'profiles' # Namespace for URLs

urlpatterns = [
    # Main profile view (displays profile, handles profile form update)
    path('', views.ProfileView.as_view(), name='profile_detail'),

    # Education URLs
    path('education/add/', views.AddEducationView.as_view(), name='add_education'),
    path('education/<int:pk>/edit/', views.EditEducationView.as_view(), name='edit_education'),
    path('education/<int:pk>/delete/', views.DeleteEducationView.as_view(), name='delete_education'),

    # Work Experience URLs
    path('experience/add/', views.AddExperienceView.as_view(), name='add_experience'),
    path('experience/<int:pk>/edit/', views.EditExperienceView.as_view(), name='edit_experience'),
    path('experience/<int:pk>/delete/', views.DeleteExperienceView.as_view(), name='delete_experience'),

    # Skill URLs
    path('skill/add/', views.AddSkillView.as_view(), name='add_skill'), # Handles POST from profile page
    path('skill/<int:pk>/delete/', views.DeleteSkillView.as_view(), name='delete_skill'), # Handles POST/GET from profile page
]