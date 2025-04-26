# interviews/admin.py

from django.contrib import admin
from .models import InterviewQuestion # Import the model to register

# Register the InterviewQuestion model with the Django admin site
@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    """ Customizes the display and filtering options for InterviewQuestion in the admin. """
    # Fields to display in the list view of questions
    list_display = ('question_text', 'category', 'difficulty')
    # Fields that can be used for filtering in the admin sidebar
    list_filter = ('category', 'difficulty')
    # Fields that can be searched
    search_fields = ('question_text', 'answer_tips', 'category')
    # Optional: Define which fields appear on the edit form and their order/grouping
    fields = ('question_text', 'category', 'difficulty', 'answer_tips')
    Optional: Use fieldsets for better organization on the edit page
    fieldsets = (
        (None, {
            'fields': ('question_text', 'category', 'difficulty')
        }),
        ('Guidance', {
            'fields': ('answer_tips',),
            'classes': ('collapse',) # Make this section collapsible
        }),
    )
