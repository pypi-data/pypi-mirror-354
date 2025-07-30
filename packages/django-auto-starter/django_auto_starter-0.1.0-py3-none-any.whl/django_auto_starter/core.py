import os
import subprocess
from yaspin import yaspin
import time
import re

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(e)

def update_settings(project_name,app_name):
    settings_path = os.path.join(project_name, "settings.py")

    with open(settings_path, "r") as d:
        content = d.read()

    if app_name not in content:
      content = content.replace(
          "INSTALLED_APPS = [",
          f"INSTALLED_APPS = [\n    '{app_name}',"
      )

    if "rest_framework" not in content:
        content = content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'rest_framework',"
        )

    if "corsheaders" not in content:
        content = content.replace(
            "INSTALLED_APPS = [",
            "INSTALLED_APPS = [\n    'corsheaders',"
        )
    if "corsheaders.middleware.CorsMiddleware" not in content:
        content = content.replace(
            "MIDDLEWARE = [",
            "MIDDLEWARE = [\n    'corsheaders.middleware.CorsMiddleware',"
        )
    if "CORS_ALLOW_ALL_ORIGINS" not in content:
        content += "\n\nCORS_ALLOW_ALL_ORIGINS = True\n"

    with open(settings_path, "w") as f:
        f.write(content)

def update_views(app_name):
    with open(f"{app_name}/views.py", "a") as f:
        f.writelines(
            "\nfrom django.http import HttpResponse\n\ndef hello(request):\n  return HttpResponse('Hello World!')\n\n"
        )
    with open(f"{app_name}/urls.py", "w") as f:
        f.write("from django.urls import path\n")
        f.write("from .views import hello\n")
        f.write('urlpatterns = [path("", hello, name="hello")]')

def rewrite_urls(project_name,app_name):
    with open(f"{project_name}/urls.py","w") as f:
        f.write("from django.contrib import admin\n")
        f.write("from django.urls import path,include\n")
        f.write("urlpatterns = [\n")
        f.write(f"path('', include('{app_name}.urls')),\n")
        f.write("path('admin/', admin.site.urls),\n")
        f.write("]")


def start_server():
    with yaspin(text="Starting django development server...", color="cyan") as spinner:
        subprocess.Popen("python manage.py runserver", shell=True)
        spinner.ok("✅ Server started at http://127.0.0.1:8000")


def create_project(project_name,app_name):
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return

    run_command("pip install django djangorestframework django-cors-headers")
    run_command(f"django-admin startproject {project_name} .")
    run_command(f"django-admin startapp {app_name}")
    update_settings(project_name,app_name)
    os.makedirs(f"{app_name}/templates/{app_name}", exist_ok=True)
    if os.path.exists(app_name):
      run_command(f"touch {app_name}/urls.py")
    print(f"\n✅ Project: {project_name} | App: {app_name} created successfully!")
    update_views(app_name)
    rewrite_urls(project_name,app_name)
    run_command("python manage.py makemigrations")
    run_command("python manage.py migrate")
    start_server()
