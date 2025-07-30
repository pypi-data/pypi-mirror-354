from .core import create_project

def main():
  import sys
  if len(sys.argv) !=3:
    print("Usage: django-auto <project_name> <app_name>")
  else:
    create_project(sys.argv[1], sys.argv[2])