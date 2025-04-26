import logging
from django.core.management.base import BaseCommand
from interviews.models import InterviewQuestion # Use relative import if needed

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the database with sample interview questions.'

    SAMPLE_QUESTIONS = [
        {'category': 'GENERAL', 'question_text': 'Tell me about yourself.', 'answer_tips': 'Focus on your relevant skills and experience. Keep it concise (1-2 minutes). Structure: Present, Past, Future.'},
        {'category': 'GENERAL', 'question_text': 'Why are you interested in this role?', 'answer_tips': 'Connect your skills/interests to the job description. Show genuine enthusiasm for the company and position. Mention specific aspects.'},
        {'category': 'GENERAL', 'question_text': 'What are your strengths?', 'answer_tips': 'Choose 2-3 strengths relevant to the job. Provide specific examples (STAR method). Avoid clichés.'},
        {'category': 'GENERAL', 'question_text': 'What are your weaknesses?', 'answer_tips': 'Choose a genuine weakness you are actively working on improving. Frame it positively. Show self-awareness.'},
        {'category': 'GENERAL', 'question_text': 'Where do you see yourself in 5 years?', 'answer_tips': 'Show ambition related to the role/industry. Emphasize learning and growth within the company if possible. Avoid overly specific or unrealistic goals.'},
        {'category': 'BEHAVIORAL', 'question_text': 'Tell me about a time you failed.', 'answer_tips': 'Use the STAR method (Situation, Task, Action, Result). Focus on what you learned and how you improved. Take responsibility.'},
        {'category': 'BEHAVIORAL', 'question_text': 'Describe a time you worked effectively under pressure.', 'answer_tips': 'STAR method. Highlight your coping mechanisms, prioritization skills, and positive outcome.'},
        {'category': 'BEHAVIORAL', 'question_text': 'How do you handle conflict with a coworker?', 'answer_tips': 'Focus on professional communication, active listening, finding common ground, and seeking resolution. Avoid blaming.'},
        {'category': 'TECHNICAL', 'question_text': 'Explain [a core concept related to the role, e.g., Object-Oriented Programming, REST APIs, SQL JOINs].', 'answer_tips': 'Define the concept clearly. Explain its purpose and benefits. Provide a simple example if possible.'},
        {'category': 'TECHNICAL', 'question_text': 'Describe a challenging technical problem you solved.', 'answer_tips': 'STAR method. Detail the problem, your approach, the tools/techniques used, and the successful outcome. Explain your thought process.'},
    ]

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Starting interview question population ---'))
        logger.info("Starting populate_questions management command.")
        added_count = 0
        skipped_count = 0
        error_count = 0

        for q_data in self.SAMPLE_QUESTIONS:
            q_text = q_data['question_text']
            try:
                obj, created = InterviewQuestion.objects.get_or_create(
                    question_text=q_text, # Use question as unique identifier
                    defaults=q_data # Provide category/tips if creating
                )
                if created:
                    logger.info(f'Added question: "{q_text[:50]}..."')
                    self.stdout.write(self.style.SUCCESS(f'+ Added: "{q_text[:50]}..."'))
                    added_count += 1
                else:
                    logger.warning(f'Skipped existing question: "{q_text[:50]}..."')
                    # Optionally update tips for existing questions:
                    # obj.category = q_data.get('category', obj.category)
                    # obj.answer_tips = q_data.get('answer_tips', obj.answer_tips)
                    # obj.save()
                    skipped_count += 1
            except Exception as e:
                logger.error(f"Error processing question '{q_text[:50]}...': {e}", exc_info=True)
                self.stderr.write(self.style.ERROR(f"! Error processing question '{q_text[:50]}...': {e}"))
                error_count += 1

        summary_msg = f'Finished question population. Added: {added_count}, Skipped: {skipped_count}, Errors: {error_count}'
        logger.info(summary_msg)
        self.stdout.write(self.style.SUCCESS(f'--- {summary_msg} ---'))