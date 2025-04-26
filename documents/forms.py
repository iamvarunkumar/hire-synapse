# documents/forms.py

from django import forms
from .models import CoverLetter # Import the CoverLetter model from the models.py in the same app

# Define the form for creating and editing CoverLetter instances
class CoverLetterForm(forms.ModelForm):
    """
    Form linked to the CoverLetter model.
    Specifies the fields to include and their widgets/styling.
    """
    class Meta:
        model = CoverLetter # The model this form is based on
        fields = ['title', 'body'] # The fields from the model to include in the form

        # Define widgets to control how fields are rendered in HTML
        widgets = {
            # Use TextInput for the title field
            'title': forms.TextInput(attrs={
                # Apply CSS classes for styling (using Tailwind CSS examples)
                # These classes match the styling used in other forms for consistency
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            }),
            # Use Textarea for the body field
            'body': forms.Textarea(attrs={
                'rows': 15, # Suggest a reasonable number of rows for the textarea
                # Apply consistent CSS classes
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            }),
        }

        # Define user-friendly labels for the form fields displayed in the template
        labels = {
            'title': 'Cover Letter Title',
            'body': 'Cover Letter Content',
        }

        # Optional: Add help text that appears below the form fields
        help_texts = {
             'title': 'A descriptive title for easy identification (e.g., "Cover Letter for Google SWE").'
             # 'body': 'Enter the full text of your cover letter here.' # Example help text for body
        }

