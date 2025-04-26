# profiles/admin.py

from django.contrib import admin
# --- Import ALL models used in this file ---
from .models import (
    UserProfile, Education, WorkExperience, Skill,
    Project, Award, Certification # <-- Added Project, Award, Certification here
)

# --- Inline classes for related models ---

class EducationInline(admin.TabularInline): # Or StackedInline
    model = Education
    extra = 0 # Show 0 empty forms by default for existing profiles

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 0

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0
    readonly_fields = ('created_at',) # Good practice for auto-added fields

class ProjectInline(admin.TabularInline):
    model = Project # Now 'Project' is defined because it was imported
    extra = 0

class AwardInline(admin.TabularInline):
    model = Award # Now 'Award' is defined
    extra = 0

class CertificationInline(admin.TabularInline):
    model = Certification # Now 'Certification' is defined
    extra = 0

# --- Main Admin class for UserProfile ---

# Register UserProfile ONCE and include all inlines
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'updated_at')
    search_fields = ('user__username', 'user__email', 'location')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at') # Good practice
    inlines = [ # List all inlines here
        EducationInline,
        WorkExperienceInline,
        SkillInline,
        ProjectInline,
        AwardInline,
        CertificationInline
    ]

# --- Admin classes for other models (Optional but good for direct management) ---

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'institution_name', 'degree', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'institution_name', 'degree', 'field_of_study')
    list_filter = ('start_date', 'end_date')
    autocomplete_fields = ['profile'] # Makes selecting the profile easier

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'job_title', 'company_name')
    list_filter = ('start_date', 'end_date')
    autocomplete_fields = ['profile']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'created_at')
    search_fields = ('profile__user__username', 'name')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ['profile']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'start_date', 'end_date')
    search_fields = ('profile__user__username', 'name', 'description')
    list_filter = ('start_date', 'end_date')
    autocomplete_fields = ['profile']

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'issuer', 'date_received')
    search_fields = ('profile__user__username', 'title', 'issuer')
    list_filter = ('date_received',)
    autocomplete_fields = ['profile']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'issuing_organization', 'issue_date', 'expiration_date')
    search_fields = ('profile__user__username', 'name', 'issuing_organization')
    list_filter = ('issue_date', 'expiration_date')
    autocomplete_fields = ['profile']

# --- Remove the redundant UserProfileAdmin registration that was here ---

