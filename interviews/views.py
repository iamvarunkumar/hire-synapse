# interviews/views.py

import logging
from django.shortcuts import render # Usually needed, even if just for potential error pages
from django.views.generic import ListView # Use ListView for displaying lists of objects
from .models import InterviewQuestion # Import the model for this app

# Get a logger instance specific to this module
logger = logging.getLogger(__name__)

class InterviewQuestionListView(ListView):
    """ Displays a list of interview questions. """
    model = InterviewQuestion # The model this view will display data from
    template_name = 'interviews/question_list.html' # The template to render
    context_object_name = 'question_list' # The variable name for the list in the template
    paginate_by = 20 # Show 20 questions per page

    def get_queryset(self):
        """
        Returns the queryset of questions to display.
        Currently fetches all questions, ordered by category and text.
        """
        logger.info("Fetching interview questions.")
        # Consider adding filtering by category later via GET params
        # category_filter = self.request.GET.get('category')
        # if category_filter:
        #     logger.info(f"Filtering interview questions by category: {category_filter}")
        #     return InterviewQuestion.objects.filter(category=category_filter).order_by('question_text')
        return InterviewQuestion.objects.all().order_by('category', 'question_text')

    # Optional: Group by category in the context if needed by the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Example: Group questions by category for display
        questions_by_category = {}
        # Use the paginated object_list from the context
        for question in context['object_list']: # Use object_list from ListView context
            cat = question.get_category_display() # Get display name
            if cat not in questions_by_category:
                questions_by_category[cat] = []
            questions_by_category[cat].append(question)
        context['questions_by_category'] = questions_by_category # Add grouped data to context
        logger.debug(f"Grouped questions by category for context.")
        return context
