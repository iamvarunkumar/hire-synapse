# HireSynapse (Global Gateway)

## Overview

HireSynapse (formerly known as Global Gateway during initial planning) is a comprehensive online platform designed to empower entry-level job seekers ("newbies") worldwide. It aims to address the common challenges faced by individuals starting their careers, such as lack of experience, difficulty creating effective application materials, and inadequate interview preparation.

The platform provides an integrated suite of tools including resume building, cover letter creation, a global job board, and resources for interview preparation and skill building.

## Features (Current & Planned)

### Implemented Features (Up to Sprint 4):

* **User Authentication:** Secure user registration, login, and logout.
* **Candidate Profiles:** Detailed user profiles including bio, summary/objective, location, and links.
* **Resume Builder:** Sections for adding/editing/deleting:
    * Education History
    * Work Experience
    * Projects
    * Awards & Honors
    * Certifications
    * Skills
* **Cover Letter Maker:** Create, view, edit, and delete cover letters.
* **Job Board:** Display job listings aggregated from various sources (currently populated with sample data).
* **Job Search:** Basic keyword search across job titles, companies, descriptions, and locations.
* **Theming:** Light/Dark mode toggle.

### Planned Features (Future Sprints):

* Advanced Job Aggregation (Scraping/APIs)
* Application Tracking System
* Interview Preparation Hub (Question database, guides)
* AI Mock Interview Practice
* Mock Interviews with Company Insiders (Unique Feature)
* Virtual Events Platform
* AI Resume/LinkedIn Analyzers
* Hands-on Experience / Skill Building Resources
* Advanced Job Search Filters
* Employer Features (Posting jobs, searching candidates)
* Community Features (Forums, Messaging)
* Globalization & Localization
* Premium Subscription Tiers

## Technology Stack

* **Backend:** Python / Django Framework
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
* **Version Control:** Git / GitHub (or GitLab/Bitbucket)
* **Hosting:** AWS / GCP (Planned)
* **Potential Future Additions:** Celery & Redis (for background tasks), WebRTC/Video APIs, AI/NLP Libraries (spaCy, NLTK), Web Scraping Libraries (Beautiful Soup, Scrapy).

## Project Setup & Local Development

Follow these steps to set up the project locally:

1.  **Prerequisites:**
    * Python 3.10+
    * `pip` (Python package installer)
    * Git
    * PostgreSQL database running

2.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd hire_synapse # Or your project's root directory name
    ```

3.  **Create and Activate Virtual Environment:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You'll need to create a `requirements.txt` file using `pip freeze > requirements.txt`)*

5.  **Environment Variables:**
    * Create a `.env` file in the project root directory (where `manage.py` is).
    * Add necessary environment variables. At minimum, you'll likely need:
        ```dotenv
        SECRET_KEY='your_strong_django_secret_key'
        DEBUG=True
        DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/DB_NAME' # e.g., postgres://postgres:password@localhost:5432/hiresynapse_db
        # Add other variables like email settings, API keys later
        ```
    * Ensure your `settings.py` is configured to read these variables (e.g., using `python-dotenv` or `django-environ`).

6.  **Database Setup:**
    * Make sure your PostgreSQL server is running.
    * Create the database specified in your `DATABASE_URL` (e.g., `hiresynapse_db`).

7.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8.  **Create Superuser (for Admin Access):**
    ```bash
    python manage.py createsuperuser
    ```
    (Follow the prompts)

9.  **Populate Sample Job Data (Optional):**
    ```bash
    python manage.py populate_jobs
    ```

10. **Run Development Server:**
    ```bash
    python manage.py runserver
    ```
    The application should now be running at `http://127.0.0.1:8000/`.

## Usage

* Navigate to `http://127.0.0.1:8000/` to see the homepage.
* Sign up or log in as a user.
* Access your profile via the navigation bar to build your resume.
* Access the "Cover Letters" section to manage cover letters.
* Access the "Jobs" section to view and search job listings.
* Access the Django admin interface at `http://127.0.0.1:8000/admin/` using your superuser credentials.


