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