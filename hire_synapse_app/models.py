# --- profiles/models.py ---

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model: Extends the default Django User model
class UserProfile(models.Model):
    """
    Stores additional information related to a user.
    Automatically created when a new User is created.
    """
    # One-to-one link with Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Basic profile fields
    bio = models.TextField(blank=True, null=True, help_text="A short biography or summary.")
    location = models.CharField(max_length=100, blank=True, null=True, help_text="City, Country")
    website = models.URLField(blank=True, null=True, help_text="Personal website or portfolio link.")
    linkedin_url = models.URLField(blank=True, null=True, help_text="LinkedIn profile URL.")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create or update UserProfile whenever a User instance is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a UserProfile when a new User is created,
    and saves the profile whenever the User object is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


# Education Model
class Education(models.Model):
    """
    Stores details about a user's educational background.
    Linked to the UserProfile.
    """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='education')
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Bachelor of Science")
    field_of_study = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Computer Science")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently studying")
    description = models.TextField(blank=True, null=True, help_text="Optional details, activities, or achievements.")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date'] # Show most recent education first

    def __str__(self):
        return f"{self.degree} at {self.institution_name} ({self.profile.user.username})"


# Work Experience Model
class WorkExperience(models.Model):
    """
    Stores details about a user's work experience.
    Linked to the UserProfile.
    """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experience')
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current job")
    description = models.TextField(blank=True, null=True, help_text="Responsibilities and achievements.")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date'] # Show most recent experience first

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.profile.user.username})"


# Skill Model
class Skill(models.Model):
    """
    Stores skills associated with a user's profile.
    """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    # Optional: Add proficiency level if needed later
    # PROFICIENCY_CHOICES = [('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')]
    # proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name'] # Order skills alphabetically

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"

# --- profiles/forms.py ---

from django import forms
from .models import UserProfile, Education, WorkExperience, Skill

class UserProfileForm(forms.ModelForm):
    """
    Form for updating the main UserProfile fields.
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'website', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'location': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'website': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        }

class EducationForm(forms.ModelForm):
    """
    Form for adding/editing Education entries.
    """
    class Meta:
        model = Education
        fields = ['institution_name', 'degree', 'field_of_study', 'start_date', 'end_date', 'description']
        widgets = {
            # Add date picker widgets if desired (e.g., forms.DateInput(attrs={'type': 'date'}))
            'institution_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'degree': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'field_of_study': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        }
        # Add labels for clarity if needed
        labels = {
            'institution_name': 'Institution Name',
            'field_of_study': 'Field of Study',
            'start_date': 'Start Date',
            'end_date': 'End Date (Leave blank if current)',
        }

class WorkExperienceForm(forms.ModelForm):
    """
    Form for adding/editing Work Experience entries.
    """
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company_name', 'location', 'start_date', 'end_date', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'company_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'location': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
        }
        labels = {
            'job_title': 'Job Title',
            'company_name': 'Company Name',
            'start_date': 'Start Date',
            'end_date': 'End Date (Leave blank if current)',
        }

class SkillForm(forms.ModelForm):
    """
    Form for adding Skills.
    """
    class Meta:
        model = Skill
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'Enter a skill'}),
        }
        labels = {
            'name': 'Skill Name',
        }


# --- profiles/views.py ---

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages # For flash messages
from .models import UserProfile, Education, WorkExperience, Skill
from .forms import UserProfileForm, EducationForm, WorkExperienceForm, SkillForm

# View to display and edit the user's profile
class ProfileView(LoginRequiredMixin, View):
    """
    Handles displaying the user's profile and processing updates for
    UserProfile, Education, WorkExperience, and Skills via separate forms.
    """
    template_name = 'profiles/profile_detail.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        # Forms for display and potential submission
        profile_form = UserProfileForm(instance=profile)
        education_form = EducationForm()
        experience_form = WorkExperienceForm()
        skill_form = SkillForm()

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'education_form': education_form,
            'experience_form': experience_form,
            'skill_form': skill_form,
            'education_list': profile.education.all(),
            'experience_list': profile.experience.all(),
            'skill_list': profile.skills.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # This view primarily handles GET. POST actions for specific sections
        # are handled by dedicated views below (AddEducationView, etc.).
        # However, we can handle the UserProfile update here if desired.
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:profile_detail') # Redirect back to profile page
        else:
            # If profile form is invalid, re-render the page with errors
            # Need to repopulate other forms and lists for the context
            education_form = EducationForm()
            experience_form = WorkExperienceForm()
            skill_form = SkillForm()
            context = {
                'profile': profile,
                'profile_form': profile_form, # Show form with errors
                'education_form': education_form,
                'experience_form': experience_form,
                'skill_form': skill_form,
                'education_list': profile.education.all(),
                'experience_list': profile.experience.all(),
                'skill_list': profile.skills.all(),
            }
            messages.error(request, 'Please correct the errors in the profile section.')
            return render(request, self.template_name, context)


# --- Views for Education ---

class AddEducationView(LoginRequiredMixin, CreateView):
    """Adds a new education entry to the user's profile."""
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html' # Generic template for add/edit
    success_url = reverse_lazy('profiles:profile_detail') # Redirect to profile page on success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Education' # Pass title to template
        return context

    def form_valid(self, form):
        # Associate the education entry with the current user's profile
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

class EditEducationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edits an existing education entry."""
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Education'
        return context

    def test_func(self):
        # Ensure the user editing the entry owns the profile it belongs to
        education = self.get_object()
        return self.request.user == education.profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

class DeleteEducationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes an education entry."""
    model = Education
    template_name = 'profiles/delete_confirm.html' # Confirmation template
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this education entry: {self.object.degree} at {self.object.institution_name}?"
        return context

    def test_func(self):
        education = self.get_object()
        return self.request.user == education.profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Education deleted successfully!')
         return super().post(request, *args, **kwargs) # Use super() for deletion logic


# --- Views for Work Experience ---

class AddExperienceView(LoginRequiredMixin, CreateView):
    """Adds a new work experience entry."""
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Work Experience'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Work Experience added successfully!')
        return super().form_valid(form)

class EditExperienceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edits an existing work experience entry."""
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Work Experience'
        return context

    def test_func(self):
        experience = self.get_object()
        return self.request.user == experience.profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Work Experience updated successfully!')
        return super().form_valid(form)

class DeleteExperienceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a work experience entry."""
    model = WorkExperience
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this experience: {self.object.job_title} at {self.object.company_name}?"
        return context

    def test_func(self):
        experience = self.get_object()
        return self.request.user == experience.profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Work Experience deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Skills ---

class AddSkillView(LoginRequiredMixin, View):
    """Adds a skill via POST request, typically from the main profile page."""
    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data['name']
            # Avoid duplicate skills for the same profile
            if not Skill.objects.filter(profile=profile, name__iexact=skill_name).exists():
                Skill.objects.create(profile=profile, name=skill_name)
                messages.success(request, f'Skill "{skill_name}" added successfully!')
            else:
                messages.warning(request, f'Skill "{skill_name}" already exists.')
        else:
             # Handle invalid form if needed, maybe display error on profile page
             messages.error(request, 'Invalid skill name.')
             # Consider passing the invalid form back to the profile template if needed
             # This requires modifying ProfileView GET to handle potential invalid skill_form

        return redirect('profiles:profile_detail') # Always redirect back

class DeleteSkillView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a skill entry."""
    model = Skill
    # No dedicated template needed if deletion happens via POST from profile page
    # template_name = 'profiles/delete_confirm.html' # Or use a confirmation page
    success_url = reverse_lazy('profiles:profile_detail')

    def test_func(self):
        skill = self.get_object()
        return self.request.user == skill.profile.user

    # Override post for flash message and potentially handle non-template deletion
    def post(self, request, *args, **kwargs):
         skill = self.get_object()
         skill_name = skill.name
         response = super().post(request, *args, **kwargs) # Perform deletion
         messages.success(self.request, f'Skill "{skill_name}" deleted successfully!')
         return response

    # If using GET request for deletion link (less secure, not recommended for delete)
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


# --- profiles/urls.py ---

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


# --- profiles/admin.py ---

from django.contrib import admin
from .models import UserProfile, Education, WorkExperience, Skill

# Customize how models appear in the admin interface

class EducationInline(admin.TabularInline): # Or StackedInline
    model = Education
    extra = 1 # Number of empty forms to display

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'updated_at')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('created_at', 'updated_at')
    inlines = [EducationInline, WorkExperienceInline, SkillInline] # Show related items directly in profile admin

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'institution_name', 'degree', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'institution_name', 'degree', 'field_of_study')
    list_filter = ('start_date', 'end_date')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'job_title', 'company_name')
    list_filter = ('start_date', 'end_date')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'created_at')
    search_fields = ('profile__user__username', 'name')
    list_filter = ('created_at',)


# --- project/urls.py (Example of including profile URLs) ---
# Make sure you have this in your main urls.py

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
"""

# --- settings.py (Add 'profiles' to INSTALLED_APPS) ---
# Ensure 'profiles.apps.ProfilesConfig' or just 'profiles' is in your INSTALLED_APPS list
"""
INSTALLED_APPS = [
    # ... other apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # Your apps
    'profiles', # Add this line
    # ... other custom apps
]
"""
