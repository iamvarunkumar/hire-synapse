# interviews/models.py

from django.db import models

class InterviewQuestion(models.Model):
    """ Stores common interview questions and tips. """
    CATEGORY_CHOICES = [
        ('BEHAVIORAL', 'Behavioral'),
        ('TECHNICAL', 'Technical'),
        ('SITUATIONAL', 'Situational'),
        ('GENERAL', 'General'),
        # Add more categories as needed
    ]

    question_text = models.TextField(unique=True) # Ensure questions are unique
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='GENERAL')
    answer_tips = models.TextField(blank=True, null=True, help_text="Tips, common answers, or things to consider.")
    difficulty = models.PositiveSmallIntegerField(default=1, help_text="Optional difficulty rating (e.g., 1-5)") # Optional

    class Meta:
        ordering = ['category', 'question_text'] # Order questions logically

    def __str__(self):
        # Provide a concise string representation for admin and debugging
        return f"{self.category} - {self.question_text[:60]}..." # Shortened representation
