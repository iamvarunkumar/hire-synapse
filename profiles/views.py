# profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# --- Corrected Model Imports ---
# Import ALL models used in this file
from .models import (
    UserProfile, Education, WorkExperience, Skill,
    Project, Award, Certification # <-- Added Project, Award, Certification
)

# --- Corrected Form Imports ---
# Import ALL forms used in this file
from .forms import (
    UserProfileForm, EducationForm, WorkExperienceForm, SkillForm,
    ProjectForm, AwardForm, CertificationForm #<-- Added ProjectForm, AwardForm, CertificationForm
)

# --- ProfileView (Updated for Sprint 3 context) ---
class ProfileView(LoginRequiredMixin, View):
    """
    Handles displaying the user's profile and processing updates for
    UserProfile. Also provides context for adding other items.
    """
    template_name = 'profiles/profile_detail.html'

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        # Forms for display and potential submission
        profile_form = UserProfileForm(instance=profile)
        # Forms needed for the "Add" buttons/modals on the profile page
        education_form = EducationForm()
        experience_form = WorkExperienceForm()
        skill_form = SkillForm()
        project_form = ProjectForm()
        award_form = AwardForm()
        certification_form = CertificationForm()

        context = {
            'profile': profile,
            'profile_form': profile_form,
            # Pass 'add' forms to the template context
            'education_form': education_form,
            'experience_form': experience_form,
            'skill_form': skill_form,
            'project_form': project_form,
            'award_form': award_form,
            'certification_form': certification_form,
            # Lists for display
            'education_list': profile.education.all(),
            'experience_list': profile.experience.all(),
            'skill_list': profile.skills.all(),
            'project_list': profile.projects.all(),
            'award_list': profile.awards.all(),
            'certification_list': profile.certifications.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """ Handles the POST request ONLY for updating the main UserProfile. """
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
            project_form = ProjectForm()
            award_form = AwardForm()
            certification_form = CertificationForm()
            context = {
                'profile': profile,
                'profile_form': profile_form, # Show form with errors
                'education_form': education_form,
                'experience_form': experience_form,
                'skill_form': skill_form,
                'project_form': project_form,
                'award_form': award_form,
                'certification_form': certification_form,
                'education_list': profile.education.all(),
                'experience_list': profile.experience.all(),
                'skill_list': profile.skills.all(),
                'project_list': profile.projects.all(),
                'award_list': profile.awards.all(),
                'certification_list': profile.certifications.all(),
            }
            messages.error(request, 'Please correct the errors in the profile section.')
            return render(request, self.template_name, context)


# --- Views for Education (Sprint 2) ---

class AddEducationView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Education'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Education added successfully!')
        return super().form_valid(form)

class EditEducationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Education'
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Education updated successfully!')
        return super().form_valid(form)

class DeleteEducationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this education entry: {self.object.degree} at {self.object.institution_name}?"
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Education deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Work Experience (Sprint 2) ---

class AddExperienceView(LoginRequiredMixin, CreateView):
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
    model = WorkExperience
    form_class = WorkExperienceForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Work Experience'
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Work Experience updated successfully!')
        return super().form_valid(form)

class DeleteExperienceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WorkExperience
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete this experience: {self.object.job_title} at {self.object.company_name}?"
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Work Experience deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Skills (Sprint 2) ---

class AddSkillView(LoginRequiredMixin, View):
    """ Adds a skill via POST request, typically from the main profile page. """
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
             messages.error(request, 'Invalid skill name.')
             # Consider passing the invalid form back via context if needed

        return redirect('profiles:profile_detail') # Always redirect back

class DeleteSkillView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Deletes a skill entry. """
    model = Skill
    success_url = reverse_lazy('profiles:profile_detail')

    def test_func(self):
        skill = self.get_object()
        return self.request.user == skill.profile.user

    # Override post for flash message and to avoid needing a confirmation template
    def post(self, request, *args, **kwargs):
         skill = self.get_object()
         skill_name = skill.name
         response = super().post(request, *args, **kwargs) # Perform deletion
         messages.success(self.request, f'Skill "{skill_name}" deleted successfully!')
         return response

    # If you want GET requests to delete (less safe), uncomment this:
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


# --- Views for Projects (Sprint 3) ---

class AddProjectView(LoginRequiredMixin, CreateView):
    model = Project # Now 'Project' is defined via import
    form_class = ProjectForm # Now 'ProjectForm' is defined via import
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Project'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Project added successfully!')
        return super().form_valid(form)

class EditProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Project'
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete the project: {self.object.name}?"
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Project deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Awards (Sprint 3) ---

class AddAwardView(LoginRequiredMixin, CreateView):
    model = Award # Now 'Award' is defined via import
    form_class = AwardForm # Now 'AwardForm' is defined via import
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Award/Honor'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Award added successfully!')
        return super().form_valid(form)

class EditAwardView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Award
    form_class = AwardForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Award/Honor'
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Award updated successfully!')
        return super().form_valid(form)

class DeleteAwardView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Award
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete the award: {self.object.title}?"
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Award deleted successfully!')
         return super().post(request, *args, **kwargs)


# --- Views for Certifications (Sprint 3) ---

class AddCertificationView(LoginRequiredMixin, CreateView):
    model = Certification # Now 'Certification' is defined via import
    form_class = CertificationForm # Now 'CertificationForm' is defined via import
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add Certification'
        return context

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        messages.success(self.request, 'Certification added successfully!')
        return super().form_valid(form)

class EditCertificationView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'profiles/add_edit_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Certification'
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def form_valid(self, form):
        messages.success(self.request, 'Certification updated successfully!')
        return super().form_valid(form)

class DeleteCertificationView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certification
    template_name = 'profiles/delete_confirm.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_message'] = f"Are you sure you want to delete the certification: {self.object.name}?"
        return context

    def test_func(self):
        return self.request.user == self.get_object().profile.user

    def post(self, request, *args, **kwargs):
         messages.success(self.request, 'Certification deleted successfully!')
         return super().post(request, *args, **kwargs)

