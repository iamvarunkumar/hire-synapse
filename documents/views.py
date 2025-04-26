# documents/views.py

from django.shortcuts import render # Not strictly needed for these Class-Based Views, but good practice
from django.urls import reverse_lazy # Used for success_url redirection
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # For access control
from django.contrib import messages # To show success/error messages to the user
from .models import CoverLetter # Import the model this app works with
from .forms import CoverLetterForm # Import the form used for creating/editing

# View to display a list of the user's cover letters
class CoverLetterListView(LoginRequiredMixin, ListView):
    """
    Displays a list of cover letters created by the currently logged-in user.
    """
    model = CoverLetter # Specifies the model to use
    template_name = 'documents/coverletter_list.html' # Template to render
    context_object_name = 'coverletter_list' # Name of the variable in the template context

    def get_queryset(self):
        """
        Overrides the default queryset to only return cover letters
        belonging to the currently logged-in user.
        """
        # Filter the default queryset (all CoverLetter objects)
        # to only include those where the 'user' field matches the request user.
        return CoverLetter.objects.filter(user=self.request.user)

# Optional: View to display details of a single cover letter
# class CoverLetterDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     """
#     Displays the details of a single cover letter.
#     (Often combined with the UpdateView for simplicity).
#     """
#     model = CoverLetter
#     template_name = 'documents/coverletter_detail.html' # Needs to be created if used
#     context_object_name = 'coverletter'
#
#     def test_func(self):
#         """
#         Ensures the user viewing the detail owns the cover letter.
#         """
#         # Get the cover letter object this view is displaying
#         cover_letter = self.get_object()
#         # Check if the logged-in user is the owner
#         return self.request.user == cover_letter.user

# View to handle the creation of a new cover letter
class CoverLetterCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the display of the form for creating a new cover letter
    and the processing of the form submission.
    """
    model = CoverLetter
    form_class = CoverLetterForm # Use the CoverLetterForm defined in forms.py
    template_name = 'documents/coverletter_form.html' # Template containing the form
    success_url = reverse_lazy('documents:coverletter_list') # Redirect to the list view on success

    def get_context_data(self, **kwargs):
        """
        Adds extra context data for the template, like a title.
        """
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Cover Letter' # Pass title to template
        return context

    def form_valid(self, form):
        """
        Called when the submitted form data is valid.
        Assigns the current user to the cover letter before saving.
        """
        # Set the 'user' field of the new CoverLetter instance
        # to the currently logged-in user before saving it to the database.
        form.instance.user = self.request.user
        # Add a success message to be displayed on the next page
        messages.success(self.request, 'Cover Letter created successfully!')
        # Call the parent class's form_valid method to handle saving and redirection
        return super().form_valid(form)

# View to handle editing an existing cover letter
class CoverLetterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Handles the display of the form pre-filled with an existing cover letter's data
    and the processing of the form submission for updates.
    """
    model = CoverLetter
    form_class = CoverLetterForm
    template_name = 'documents/coverletter_form.html' # Reuse the form template
    success_url = reverse_lazy('documents:coverletter_list') # Redirect to list view on success

    def get_context_data(self, **kwargs):
        """ Adds extra context data for the template. """
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Cover Letter' # Pass title to template
        return context

    def test_func(self):
        """
        Ensures the user trying to edit the cover letter is the owner.
        UserPassesTestMixin runs this check before displaying the view.
        """
        cover_letter = self.get_object() # Get the object being updated
        return self.request.user == cover_letter.user # Check ownership

    def form_valid(self, form):
        """ Called when the submitted form data is valid. """
        # Add a success message
        messages.success(self.request, 'Cover Letter updated successfully!')
        # Let the parent class handle saving and redirection
        return super().form_valid(form)

# View to handle the deletion of a cover letter
class CoverLetterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Handles the display of the confirmation page for deleting a cover letter
    and processes the actual deletion upon confirmation (POST request).
    """
    model = CoverLetter
    template_name = 'documents/coverletter_confirm_delete.html' # Confirmation template
    success_url = reverse_lazy('documents:coverletter_list') # Redirect to list view after deletion
    context_object_name = 'coverletter' # Name for the object in the template context

    def test_func(self):
        """ Ensures the user trying to delete the cover letter is the owner. """
        cover_letter = self.get_object()
        return self.request.user == cover_letter.user

    # Override post to add the success message *after* deletion
    def post(self, request, *args, **kwargs):
        """ Handles the POST request to confirm deletion. """
        # Add success message before calling the parent's deletion logic
        messages.success(self.request, 'Cover Letter deleted successfully!')
        # Call the parent DeleteView's post method to perform the deletion
        return super().post(request, *args, **kwargs)

