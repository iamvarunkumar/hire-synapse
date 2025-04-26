from django.shortcuts import render
from django.views.generic import ListView
from .models import JobPosting
from django.db.models import Q # For complex lookups (OR conditions)

class JobListSearchView(ListView):
    """ Displays a list of job postings and handles search queries. """
    model = JobPosting
    template_name = 'jobs/job_list.html'
    context_object_name = 'job_list'
    paginate_by = 15 # Show 15 jobs per page

    def get_queryset(self):
        """ Filter jobs based on search query parameter 'q'. """
        queryset = super().get_queryset() # Get all JobPostings initially
        query = self.request.GET.get('q') # Get the search term from URL (?q=...)

        if query:
            # Perform case-insensitive search across multiple fields
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company_name__icontains=query) |
                Q(location__icontains=query)
            ).distinct() # Use distinct() if Q objects might cause duplicates

        return queryset

    def get_context_data(self, **kwargs):
        """ Add the search query back to the context to display in the form. """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '') # Pass query back to template
        return context