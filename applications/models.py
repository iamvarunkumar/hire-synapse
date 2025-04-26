# applications/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jobs.models import JobPosting # Import JobPosting from the jobs app

class Application(models.Model):
    """ Represents a job application tracked by a user. """

    # Status choices for the application lifecycle
    STATUS_CHOICES = [
        ('WISHLIST', 'Wishlist'),
        ('APPLIED', 'Applied'),
        ('SCREENING', 'Screening'),
        ('INTERVIEWING', 'Interviewing'),
        ('ASSESSMENT', 'Assessment'),
        ('OFFER', 'Offer Received'),
        ('REJECTED', 'Rejected'),
        ('DECLINED', 'Offer Declined'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    # Link to a job posting from our board (optional)
    job_posting = models.ForeignKey(
        JobPosting,
        on_delete=models.SET_NULL, # Keep application even if job posting is deleted
        null=True,
        blank=True,
        related_name='applications'
    )
    # Manual entry fields (required if job_posting is not set, potentially redundant otherwise)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    # Location can be inferred from job_posting if linked, or entered manually
    location = models.CharField(max_length=150, blank=True, null=True)

    # Tracking fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WISHLIST')
    date_applied = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Your personal notes about this application.")
    application_url = models.URLField(max_length=500, blank=True, null=True, help_text="Link to the application portal or job description.")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] # Show most recently updated first

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.user.username})"

    # Optional: Pre-populate fields if job_posting is selected
    # def save(self, *args, **kwargs):
    #     if self.job_posting and not self.pk: # If linked job and creating new application
    #         if not self.company_name:
    #             self.company_name = self.job_posting.company_name
    #         if not self.job_title:
    #             self.job_title = self.job_posting.title
    #         if not self.location:
    #              self.location = self.job_posting.location
    #         if not self.application_url:
    #              self.application_url = self.job_posting.job_url
    #     super().save(*args, **kwargs)


# applications/forms.py

from django import forms
from .models import Application
from jobs.models import JobPosting # Needed for ModelChoiceField

class ApplicationForm(forms.ModelForm):
    """ Form for creating and editing Job Applications. """

    # Optional: Allow selecting a job from the board to pre-fill details
    # Use ModelChoiceField, make it not required
    job_posting_select = forms.ModelChoiceField(
        queryset=JobPosting.objects.order_by('-date_added_db'), # Show newest jobs first
        required=False,
        label="Link to Job Posting (Optional)",
        help_text="Select a job from the board to pre-fill details.",
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            })
    )

    class Meta:
        model = Application
        # Exclude user (set in view), created_at, updated_at
        fields = [
            'job_posting_select', # Add the selection field
            'company_name',
            'job_title',
            'location',
            'status',
            'date_applied',
            'application_url',
            'notes',
        ]
        widgets = {
            # Apply consistent styling
            'company_name': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'job_title': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'location': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'status': forms.Select(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'date_applied': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'application_url': forms.URLInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
            'notes': forms.Textarea(attrs={'rows': 5, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'}),
        }
        labels = {
            'company_name': 'Company Name',
            'job_title': 'Job Title',
            'date_applied': 'Date Applied (Optional)',
            'application_url': 'Application/Job URL (Optional)',
            'notes': 'Notes',
        }

    def clean(self):
        """ Add custom validation if needed. """
        cleaned_data = super().clean()
        job_posting = cleaned_data.get('job_posting_select')
        company_name = cleaned_data.get('company_name')
        job_title = cleaned_data.get('job_title')

        # Require company/title if no job posting is linked
        if not job_posting:
            if not company_name:
                self.add_error('company_name', 'Company name is required if not linking to a job posting.')
            if not job_title:
                 self.add_error('job_title', 'Job title is required if not linking to a job posting.')

        return cleaned_data


# applications/views.py

import logging
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Application
from .forms import ApplicationForm

logger = logging.getLogger(__name__)

class ApplicationListView(LoginRequiredMixin, ListView):
    """ Displays a list of the user's job applications. """
    model = Application
    template_name = 'applications/application_list.html'
    context_object_name = 'application_list'
    paginate_by = 10 # Show 10 applications per page

    def get_queryset(self):
        """ Only show applications belonging to the logged-in user. """
        queryset = Application.objects.filter(user=self.request.user).order_by('-updated_at')
        logger.info(f"Fetching applications for user {self.request.user.username}")
        return queryset

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    """ Handles creating a new job application entry. """
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/application_form.html'
    success_url = reverse_lazy('applications:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add New Application'
        return context

    def form_valid(self, form):
        """ Assign user and handle potential job posting link before saving. """
        form.instance.user = self.request.user
        job_posting = form.cleaned_data.get('job_posting_select')
        if job_posting:
            form.instance.job_posting = job_posting
            # Pre-fill fields if empty (optional, can also be done in JS)
            if not form.instance.company_name:
                form.instance.company_name = job_posting.company_name
            if not form.instance.job_title:
                form.instance.job_title = job_posting.title
            if not form.instance.location:
                 form.instance.location = job_posting.location
            if not form.instance.application_url:
                 form.instance.application_url = job_posting.job_url

        logger.info(f"User {self.request.user.username} creating application for {form.instance.job_title} at {form.instance.company_name}")
        messages.success(self.request, 'Application added successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid application form submission by user {self.request.user.username}: {form.errors}")
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Handles editing an existing job application entry. """
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/application_form.html'
    success_url = reverse_lazy('applications:application_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Application'
        return context

    def get_initial(self):
        """ Pre-select the job_posting_select field if the application is linked. """
        initial = super().get_initial()
        if self.object.job_posting:
            initial['job_posting_select'] = self.object.job_posting.pk
        return initial

    def test_func(self):
        """ Ensure user owns the application they are trying to edit. """
        application = self.get_object()
        return self.request.user == application.user

    def form_valid(self, form):
        """ Handle potential job posting link update. """
        job_posting = form.cleaned_data.get('job_posting_select')
        form.instance.job_posting = job_posting # Update or clear the link
        # Optionally re-fill fields if job_posting was changed, or leave as is
        logger.info(f"User {self.request.user.username} updated application (ID: {self.object.pk})")
        messages.success(self.request, 'Application updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Invalid application update form submission by user {self.request.user.username} (ID: {self.object.pk}): {form.errors}")
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Handles deleting a job application entry. """
    model = Application
    template_name = 'applications/application_confirm_delete.html'
    success_url = reverse_lazy('applications:application_list')
    context_object_name = 'application'

    def test_func(self):
        """ Ensure user owns the application they are trying to delete. """
        application = self.get_object()
        return self.request.user == application.user

    def post(self, request, *args, **kwargs):
        app_id = self.get_object().pk
        app_title = str(self.get_object())
        logger.warning(f"User {request.user.username} deleting application '{app_title}' (ID: {app_id})")
        messages.success(self.request, 'Application deleted successfully!')
        return super().post(request, *args, **kwargs)


# applications/urls.py

from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application_list'),
    path('add/', views.ApplicationCreateView.as_view(), name='application_add'),
    path('<int:pk>/edit/', views.ApplicationUpdateView.as_view(), name='application_edit'),
    path('<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
]


# applications/admin.py

from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'user', 'status', 'date_applied', 'updated_at')
    list_filter = ('status', 'user', 'date_applied', 'updated_at')
    search_fields = ('job_title', 'company_name', 'user__username', 'notes')
    autocomplete_fields = ['user', 'job_posting'] # Make linking easier
    list_editable = ('status',) # Allow quick status updates from list view
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'job_posting')
        }),
        ('Manual Job Details', {
            'fields': ('company_name', 'job_title', 'location', 'application_url')
        }),
        ('Tracking Details', {
            'fields': ('status', 'date_applied', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Hide by default
        }),
    )

