#This file is basically the project's remote control
#You tell it "runserver", "migrate", etc. and it says the same to Django 
#If something doesn't wotk here is probably because the virtualenv is not active
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    #Point Django to our settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    #Hand the command you typed in the terminal to Django
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
