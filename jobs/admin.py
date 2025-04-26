from django.contrib import admin
from .models import JobPosting

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'source', 'location', 'date_added_db')
    search_fields = ('title', 'company_name', 'description', 'location', 'source')
    list_filter = ('source', 'date_added_db', 'location')
    readonly_fields = ('date_added_db',) # Prevent manual editing of this field