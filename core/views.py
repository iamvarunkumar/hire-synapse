# core/views.py

from django.shortcuts import render # Optional for TemplateView, but good practice
from django.views.generic import TemplateView # Import TemplateView

# Define the view for the homepage
class HomePageView(TemplateView):
    """
    Renders the main landing page using a specified template.
    TemplateView is a generic class-based view provided by Django
    that simplifies rendering a template without much custom logic.
    """
    # Specify the template file to be rendered when this view is accessed
    template_name = "core/home.html"

    # Optional: You can add context data to pass to the template if needed
    # def get_context_data(self, **kwargs):
    #     # Get the default context from the parent class
    #     context = super().get_context_data(**kwargs)
    #     # Add custom context variables
    #     context['page_title'] = 'Welcome!'
    #     context['featured_content'] = SomeModel.objects.filter(featured=True)
    #     # Return the updated context dictionary
    #     return context

