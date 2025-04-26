from django.db import models
from django.utils import timezone

class JobPosting(models.Model):
    """ Represents a job posting aggregated from various sources. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=150, blank=True, null=True)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_url = models.URLField(max_length=500, unique=True)
    source = models.CharField(max_length=100, help_text="e.g., LinkedIn, Indeed, Company Website")
    date_posted_source = models.DateTimeField(blank=True, null=True, help_text="Original posting date if available")
    date_added_db = models.DateTimeField(default=timezone.now, help_text="Date added to our database")

    class Meta:
        ordering = ['-date_added_db']

    def __str__(self):
        return f"{self.title} at {self.company_name} ({self.source})"