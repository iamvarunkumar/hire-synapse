from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages # For flash messages
from .models import UserProfile, Education, WorkExperience, Skill
from .forms import UserProfileForm, EducationForm, WorkExperienceForm, SkillForm

# View to display and edit the user's profile
class ProfileView(LoginRequiredMixin, View):
    """
    Handles displaying the user's profile and processing updates for
    UserProfile, Education, WorkExperience, and Skills via separate forms.
    """
    template_name = 'profiles/profile_detail.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        # Forms for display and potential submission
        profile_form = UserProfileForm(instance=profile)
        education_form = EducationForm()
        experience_form = WorkExperienceForm()
        skill_form = SkillForm()

        context = {
            'profile': profile,
            'profile_form': profile_form,
            'education_form': education_form,
            'experience_form': experience_form,
            'skill_form': skill_form,
            'education_list': profile.education.all(),
            'experience_list': profile.experience.all(),
            'skill_list': profile.skills.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # This view primarily handles GET. POST actions for specific sections
        # are handled by dedicated views below (AddEducationView, etc.).
        # However, we can handle the UserProfile update here if desired.
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profiles:profile_detail') # Redirect back to profile page
        else:
            # If profile form is invalid, re-render the page with errors
            # Need to repopulate other forms and lists for the context
            education_form = EducationForm()
            experience_form = WorkExperienceForm()
            skill_form = SkillForm()
            context = {
                'profile': profile,
                'profile_form': profile_form, # Show form with errors
                'education_form': education_form,
                'experience_form': experience_form,
                'skill_form': skill_form,
                'education_list': profile.education.all(),
                'experience_list': profile.experience.all(),
                'skill_list': profile.skills.all(),
            }
            messages.error(request, 'Please correct the errors in the profile section.')
            return render(request, self.template_name, context)


# --- Views for Education ---

class AddEducationView(LoginRequiredMixin, CreateView):
    """Adds a new education entry to the user's profile."""
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html' # Generic template for add/edit
    success_url = reverse_lazy('profiles:profile_detail') # Redirect to profile page on success

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Education' # Pass title to template
        return context

    def form_valid(self, form):
        # Associate the education entry with the current user's profile
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

class EditEducationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edits an existing education entry."""
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Education'
        return context

    def test_func(self):
        # Ensure the user editing the entry owns the profile it belongs to
        education = self.get_object()
        return self.request.user == education.profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

class DeleteEducationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes an education entry."""
    model = Education
    template_name = 'profiles/delete_confirm.html' # Confirmation template
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this education entry: {self.object.degree} at {self.object.institution_name}?"
        return context

    def test_func(self):
        education = self.get_object()
        return self.request.user == education.profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Education deleted successfully!')
         return super().post(request, *args, **kwargs) # Use super() for deletion logic


# --- Views for Work Experience ---

class AddExperienceView(LoginRequiredMixin, CreateView):
    """Adds a new work experience entry."""
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Work Experience'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Work Experience added successfully!')
        return super().form_valid(form)

class EditExperienceView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edits an existing work experience entry."""
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Work Experience'
        return context

    def test_func(self):
        experience = self.get_object()
        return self.request.user == experience.profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Work Experience updated successfully!')
        return super().form_valid(form)

class DeleteExperienceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a work experience entry."""
    model = WorkExperience
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this experience: {self.object.job_title} at {self.object.company_name}?"
        return context

    def test_func(self):
        experience = self.get_object()
        return self.request.user == experience.profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Work Experience deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Skills ---

class AddSkillView(LoginRequiredMixin, View):
    """Adds a skill via POST request, typically from the main profile page."""
    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data['name']
            # Avoid duplicate skills for the same profile
            if not Skill.objects.filter(profile=profile, name__iexact=skill_name).exists():
                Skill.objects.create(profile=profile, name=skill_name)
                messages.success(request, f'Skill "{skill_name}" added successfully!')
            else:
                messages.warning(request, f'Skill "{skill_name}" already exists.')
        else:
             # Handle invalid form if needed, maybe display error on profile page
             messages.error(request, 'Invalid skill name.')
             # Consider passing the invalid form back to the profile template if needed
             # This requires modifying ProfileView GET to handle potential invalid skill_form

        return redirect('profiles:profile_detail') # Always redirect back

class DeleteSkillView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a skill entry."""
    model = Skill
    # No dedicated template needed if deletion happens via POST from profile page
    # template_name = 'profiles/delete_confirm.html' # Or use a confirmation page
    success_url = reverse_lazy('profiles:profile_detail')

    def test_func(self):
        skill = self.get_object()
        return self.request.user == skill.profile.user

    # Override post for flash message and potentially handle non-template deletion
    def post(self, request, *args, **kwargs):
         skill = self.get_object()
         skill_name = skill.name
         response = super().post(request, *args, **kwargs) # Perform deletion
         messages.success(self.request, f'Skill "{skill_name}" deleted successfully!')
         return response

    # If using GET request for deletion link (less secure, not recommended for delete)
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)