from django.urls import path
from . import views

app_name = 'profiles' # Namespace for URLs

urlpatterns = [
    # --- Keep existing paths ---
    path('', views.ProfileView.as_view(), name='profile_detail'),
    path('education/add/', views.AddEducationView.as_view(), name='add_education'),
    path('education/<int:pk>/edit/', views.EditEducationView.as_view(), name='edit_education'),
    path('education/<int:pk>/delete/', views.DeleteEducationView.as_view(), name='delete_education'),
    path('experience/add/', views.AddExperienceView.as_view(), name='add_experience'),
    path('experience/<int:pk>/edit/', views.EditExperienceView.as_view(), name='edit_experience'),
    path('experience/<int:pk>/delete/', views.DeleteExperienceView.as_view(), name='delete_experience'),
    path('skill/add/', views.AddSkillView.as_view(), name='add_skill'),
    path('skill/<int:pk>/delete/', views.DeleteSkillView.as_view(), name='delete_skill'),

    # --- NEW URLs for Sprint 3 ---
    # Project URLs
    path('project/add/', views.AddProjectView.as_view(), name='add_project'),
    path('project/<int:pk>/edit/', views.EditProjectView.as_view(), name='edit_project'),
    path('project/<int:pk>/delete/', views.DeleteProjectView.as_view(), name='delete_project'),

    # Award URLs
    path('award/add/', views.AddAwardView.as_view(), name='add_award'),
    path('award/<int:pk>/edit/', views.EditAwardView.as_view(), name='edit_award'),
    path('award/<int:pk>/delete/', views.DeleteAwardView.as_view(), name='delete_award'),

    # Certification URLs
    path('certification/add/', views.AddCertificationView.as_view(), name='add_certification'),
    path('certification/<int:pk>/edit/', views.EditCertificationView.as_view(), name='edit_certification'),
    path('certification/<int:pk>/delete/', views.DeleteCertificationView.as_view(), name='delete_certification'),
    # --- End NEW URLs ---
]