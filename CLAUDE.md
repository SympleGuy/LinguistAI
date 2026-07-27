# LinguistAI - Language Learning Platform

## Overview
LinguistAI is a Django-based web application that helps users practice real-life conversations in various languages using AI-powered tutors. Users can practice scenarios like ordering food at a restaurant, checking into a hotel, job interviews, and more, with real-time feedback on pronunciation, grammar, and vocabulary.

## Tech Stack
- **Backend**: Django 4.2
- **Authentication & Database**: Supabase (PostgreSQL)
- **Frontend**: 
  - Main interface: linguistAi_web.html (single-page app with JavaScript routing)
  - Auth views: Django templates (base.html, login.html, register.html, dashboard.html, home.html)
  - Styling: Bootstrap 5.3
  - Icons: Bootstrap Icons
  - Fonts: Google Fonts (DM Sans)
  - Interactivity: htmx for dynamic updates
- **Environment**: Python with python-dotenv for environment management

## Project Structure
```
/LinguistAI
├── linguistAi_web.html          # Main frontend SPA (contains all pages: landing, scenarios, conversation, dashboard, profile, login)
├── myapp/                       # Django application
│   ├── views.py                 # View functions (auth, dashboard)
│   ├── urls.py                  # URL routing
│   ├── supabase_client.py       # Supabase client configuration
│   └── templates/               # Django templates (used for auth flows)
│       ├── base.html
│       ├── home.html
│       ├── dashboard.html
│       ├── login.html
│       └── register.html
├── templates/                   # Additional Django templates (duplicate of myapp/templates/)
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview
└── .gitignore                   # Git ignore file
```

## Key Features
- **Scenario-based learning**: Practice real-life conversations in various contexts
- **Multi-language support**: 30+ languages from beginner to advanced levels
- **Real-time AI feedback**: Instant feedback on pronunciation, grammar, and vocabulary
- **Progress tracking**: Dashboard showing session history, scores, and streaks
- **Voice interaction**: Microphone input simulation for speaking practice
- **Vocabulary building**: Contextual vocabulary suggestions during conversations
- **Responsive design**: Works on desktop and mobile devices

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up Supabase:
   - Create a Supabase project
   - Get your SUPABASE_URL, SUPABASE_ANON_KEY, and SUPABASE_SERVICE_ROLE_KEY
   - Create a `.env` file in the root directory with these variables
4. Run migrations: `python manage.py migrate`
5. Create a superuser (if needed): `python manage.py createsuperuser`
6. Start the development server: `python manage.py runserver`

## Development Guidelines
- Follow Django conventions for views, URLs, and templates
- Keep frontend modifications consistent with the existing Bootstrap 5.3 styling
- When modifying linguistAi_web.html, ensure responsiveness is maintained
- For Supabase interactions, use the existing supabase_client.py module
- Keep user authentication flows secure - don't expose secret keys
- Test new scenarios thoroughly across different languages and proficiency levels
- The main frontend (linguistAi_web.html) uses JavaScript for page navigation - avoid full page reloads when possible
- Auth views (login, register) use Django templates - maintain consistency with base.html styling

## Important Notes
- The main frontend is a single-page application (linguistAi_web.html) that uses JavaScript to show/hide different sections (landing, scenarios, conversation, dashboard, profile)
- Authentication flows (login/register) use traditional Django views and templates
- Supabase handles user authentication and stores user profiles, scenarios, and progress data
- Environment variables should never be committed to version control
- The application uses htmx for some dynamic updates in the linguistAi_web.html interface

## Common Development Tasks
### Running the Development Server
```bash
python manage.py runserver
```

### Running Tests (if any exist)
```bash
python manage.py test
```

### Creating New Scenarios
1. Add new scenario objects to the SCENARIOS array in linguistAi_web.html
2. Include appropriate messages, feedback, and vocabulary
3. Ensure proper categorization and CEFR levels
4. Test responsiveness on different screen sizes

### Modifying Styles
- Edit the CSS variables in the <style> section of linguistAi_web.html for global theme changes
- For component-specific styling, add to existing CSS blocks or create new ones
- Maintain consistency with Bootstrap 5.3 utility classes when possible

### Working with Supabase
- Use supabase_client.py for all database operations
- The supabase client handles user authentication
- The supabase_admin client (using service role key) should be used for administrative operations
- Never expose the service role key in client-side code

## Database Schema (Supabase)
Key tables include:
- `users`: Stores user information (id, username, target_language, proficiency_level, subscription_plan)
- Additional tables for scenarios, conversations, feedback, and vocabulary would be defined in Supabase