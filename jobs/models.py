from django.db import models
from django.utils import timezone

class JobPosting(models.Model):
    """ Represents a job posting aggregated from various sources. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255) # Keep simple for now
    location = models.CharField(max_length=150, blank=True, null=True) # e.g., "London, UK", "Remote"
    salary_range = models.CharField(max_length=100, blank=True, null=True) # e.g., "$80k - $100k", "Competitive"
    job_url = models.URLField(max_length=500, unique=True) # URL to the original posting, unique to avoid duplicates
    source = models.CharField(max_length=100, help_text="e.g., LinkedIn, Indeed, Company Website") # Source where the job was found
    date_posted_source = models.DateTimeField(blank=True, null=True, help_text="Original posting date if available") # Date from the source
    date_added_db = models.DateTimeField(default=timezone.now, help_text="Date added to our database") # Date we added it

    class Meta:
        ordering = ['-date_added_db'] # Show newest jobs first by default

    def __str__(self):
        return f"{self.title} at {self.company_name} ({self.source})"