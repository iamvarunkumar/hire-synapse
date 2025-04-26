# profiles/apps.py
from django.apps import AppConfig

# Make sure the class name is sensible, e.g., ProfilesConfig
class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles' # <--- CORRECTED LINE