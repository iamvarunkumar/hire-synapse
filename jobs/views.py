import logging # Import the logging library
from django.shortcuts import render
from django.views.generic import ListView
from .models import JobPosting
from django.db.models import Q
from django.core.paginator import Paginator # Import Paginator if handling errors manually

# Get an instance of a logger for this module
logger = logging.getLogger(__name__) # Standard practice: use module name

class JobListSearchView(ListView):
    """ Displays a list of job postings and handles search queries. """
    model = JobPosting
    template_name = 'jobs/job_list.html'
    context_object_name = 'job_list'
    paginate_by = 15

    def get_queryset(self):
        """ Filter jobs based on search query parameter 'q'. """
        logger.info("Fetching job queryset...") # Log entry point
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            logger.info(f"Search query received: '{query}'")
            try:
                queryset = queryset.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(company_name__icontains=query) |
                    Q(location__icontains=query)
                ).distinct()
                logger.info(f"Found {queryset.count()} jobs matching query.")
            except Exception as e:
                # Log unexpected errors during filtering
                logger.error(f"Error filtering job queryset for query '{query}': {e}", exc_info=True)
                # Optionally, return an empty queryset or handle differently
                queryset = JobPosting.objects.none() # Return empty on error
        else:
             logger.info("No search query provided, returning all jobs.")

        return queryset

    def get_context_data(self, **kwargs):
        """ Add the search query back to the context. """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        # Log basic context info
        logger.debug(f"Context prepared for job list view. Page: {context.get('page_obj').number if context.get('page_obj') else 'N/A'}")
        return context

    # Optional: More granular error handling for pagination (Django handles most common cases)
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e: # Catch broader errors if needed
            logger.error(f"Unhandled error in JobListSearchView GET request: {e}", exc_info=True)
            # Render an error template or return an HttpResponseServerError
            # return render(request, '500.html', status=500)
            raise # Re-raise for Django's default error handling