# documents/models.py

from django.db import models
from django.contrib.auth.models import User # Import the standard User model
from django.urls import reverse # Used for get_absolute_url

# Define the CoverLetter model
class CoverLetter(models.Model):
    """ Stores user-created cover letters. """
    # Link to the user who owns this cover letter.
    # If the user is deleted, their cover letters are also deleted (CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cover_letters')

    # Title for the cover letter for easy identification by the user.
    title = models.CharField(max_length=255, help_text="e.g., 'Cover Letter for Software Engineer at Google'")

    # The main content of the cover letter.
    body = models.TextField(help_text="The content of the cover letter.")

    # Optional: Link to a specific job application later (Commented out for now)
    # job_application = models.ForeignKey('applications.Application', null=True, blank=True, on_delete=models.SET_NULL)

    # Timestamps for tracking creation and last update.
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True) # Automatically set when saved

    class Meta:
        # Default ordering for cover letters when queried.
        # Show most recently updated ones first.
        ordering = ['-updated_at']

    def __str__(self):
        """ String representation of the CoverLetter object (used in admin, etc.). """
        return f"{self.title} ({self.user.username})"

    def get_absolute_url(self):
        """
        Returns the canonical URL for a specific cover letter instance.
        Used by Django's generic views (like CreateView, UpdateView) after successful form submission
        if `success_url` is not explicitly defined in the view.
        Note: We defined success_url in the views, so this isn't strictly necessary there,
              but it's good practice to define it for models.
        Requires a URL pattern named 'coverletter_detail' in documents/urls.py if used.
        Since we are using 'coverletter_edit' mostly, this might not be hit often.
        """
        # Assumes you have a URL pattern named 'coverletter_edit' that takes a primary key (pk)
        return reverse('documents:coverletter_edit', kwargs={'pk': self.pk})

