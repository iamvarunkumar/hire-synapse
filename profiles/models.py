# --- profiles/models.py ---

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model: Extends the default Django User model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, help_text="A short biography or summary.")
    # --- NEW FIELD for Sprint 3 ---
    summary = models.TextField(blank=True, null=True, help_text="Professional summary or objective for your resume.")
    # --- End NEW FIELD ---
    location = models.CharField(max_length=100, blank=True, null=True, help_text="City, Country")
    website = models.URLField(blank=True, null=True, help_text="Personal website or portfolio link.")
    linkedin_url = models.URLField(blank=True, null=True, help_text="LinkedIn profile URL.")
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

class Project(models.Model):
    """ Stores details about personal or professional projects. """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True, help_text="Link to project demo or repository.")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'name']

    def __str__(self):
        return f"{self.name} ({self.profile.user.username})"

class Award(models.Model):
    """ Stores details about awards or honors received. """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Organization, Competition")
    date_received = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_received', 'title']

    def __str__(self):
        return f"{self.title} ({self.profile.user.username})"

class Certification(models.Model):
    """ Stores details about certifications obtained. """
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    credential_id = models.CharField(max_length=255, blank=True, null=True)
    credential_url = models.URLField(blank=True, null=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', 'name']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization} ({self.profile.user.username})"

