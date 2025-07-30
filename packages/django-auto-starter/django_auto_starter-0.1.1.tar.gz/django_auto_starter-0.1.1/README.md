# django-auto-starter

🚀 A CLI tool for backend developers to **automatically set up a Django project** with everything needed for a REST API backend in production.

## ✨ Features

- Installs Django, Django REST Framework, and CORS headers
- Creates a Django project and a default app
- Configures `settings.py`:
  - Adds `'rest_framework'`, `'corsheaders'`, and your app to `INSTALLED_APPS`
  - Adds CORS middleware
  - Enables CORS for all origins
- Starts the Django development server with a loading spinner
- Sets up a basic template directory: `your_app/templates/your_app`

## 📦 Installation

```bash
pip install django-auto-starter
```

##  Usage

```bash
django-auto <project_name> <app_name>
```
