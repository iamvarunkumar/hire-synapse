import logging # Import logging
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import IntegrityError # Import specific database errors if needed
from jobs.models import JobPosting

# Get an instance of a logger for this command
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with sample job postings.'

    # Define sample data
    SAMPLE_JOBS = [
        # ... (keep sample job data as before) ...
        {
            'title': 'Junior Python Developer',
            'description': 'Exciting opportunity for a junior developer proficient in Python and Django. Work on web applications, APIs, and data processing tasks. Requires 1+ year experience or strong portfolio.',
            'company_name': 'Tech Solutions Inc.',
            'location': 'New Delhi, India',
            'salary_range': '₹5,00,000 - ₹8,00,000 PA',
            'job_url': 'https://example.com/job/python-dev-1',
            'source': 'Example Job Board',
            'date_posted_source': timezone.now() - datetime.timedelta(days=2),
        },
        {
            'title': 'Frontend Developer (React)',
            'description': 'Join our team to build modern user interfaces using React, HTML, and CSS. Experience with state management and REST APIs needed. Remote work possible.',
            'company_name': 'Creative Designs Ltd.',
            'location': 'Remote',
            'salary_range': '$70,000 - $90,000 USD',
            'job_url': 'https://example.com/job/frontend-react-2',
            'source': 'LinkedIn',
            'date_posted_source': timezone.now() - datetime.timedelta(days=5),
        },
        {
            'title': 'Data Analyst Intern',
            'description': 'Internship opportunity for students or recent graduates interested in data analysis. Learn SQL, Python (Pandas), and data visualization tools.',
            'company_name': 'Global Analytics Co.',
            'location': 'Mumbai, India',
            'salary_range': 'Stipend Provided',
            'job_url': 'https://example.com/job/data-intern-3',
            'source': 'Company Website',
            'date_posted_source': timezone.now() - datetime.timedelta(days=1),
        },
         {
            'title': 'Software Engineer - Entry Level',
            'description': 'Seeking passionate entry-level software engineers. Opportunity to work with various technologies including Java, Python, and cloud platforms. Strong problem-solving skills required.',
            'company_name': 'Innovatech',
            'location': 'Bengaluru, India',
            'salary_range': 'Competitive',
            'job_url': 'https://example.com/job/swe-entry-4',
            'source': 'Indeed',
            'date_posted_source': timezone.now() - datetime.timedelta(days=10),
        },
    ]

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Starting job population script ---'))
        logger.info("Starting populate_jobs management command.")
        added_count = 0
        skipped_count = 0
        error_count = 0

        for job_data in self.SAMPLE_JOBS:
            job_title = job_data.get('title', 'N/A') # Get title for logging
            job_url = job_data.get('job_url', 'N/A')
            try:
                # Use get_or_create to avoid adding duplicates based on job_url
                job, created = JobPosting.objects.get_or_create(
                    job_url=job_url, # Use URL as the unique identifier
                    defaults=job_data # Provide the rest of the data if creating
                )

                if created:
                    # Log success at INFO level
                    logger.info(f'Successfully added job: "{job_title}" (URL: {job_url})')
                    self.stdout.write(self.style.SUCCESS(f'+ Added: "{job_title}"'))
                    added_count += 1
                else:
                    # Log skipped duplicates at WARNING level
                    logger.warning(f'Skipped existing job: "{job_title}" (URL: {job_url})')
                    self.stdout.write(self.style.WARNING(f'= Skipped: "{job_title}"'))
                    skipped_count += 1
            except IntegrityError as e:
                # Log database integrity errors (e.g., unique constraint violation if get_or_create fails somehow)
                logger.error(f"Database IntegrityError adding job '{job_title}' (URL: {job_url}): {e}", exc_info=True)
                self.stderr.write(self.style.ERROR(f"! Error adding job '{job_title}': {e}"))
                error_count += 1
            except Exception as e:
                # Log any other unexpected errors during processing of a single job
                logger.error(f"Unexpected error processing job '{job_title}' (URL: {job_url}): {e}", exc_info=True)
                self.stderr.write(self.style.ERROR(f"! Error processing job '{job_title}': {e}"))
                error_count += 1

        # Log summary at INFO level
        summary_msg = f'Finished job population. Added: {added_count}, Skipped: {skipped_count}, Errors: {error_count}'
        logger.info(summary_msg)
        self.stdout.write(self.style.SUCCESS(f'--- {summary_msg} ---'))