# standrd django entry point for runnig server or migrations
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os #let interact with os
import sys # give acces to sysleve; parameter like cmd args

 #fro runing the server or applying migrations
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmaster_backend.settings') #default setting module django should use for this project. required before any django features like db access
    try:
        from django.core.management import execute_from_command_line # import to excute cmd like runserver, makemigrations, migrate, createsuperuser 
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc # if django is missing or v env is not active
    execute_from_command_line(sys.argv) # excute cmd that user enter in terminal


if __name__ == '__main__':
    main()
