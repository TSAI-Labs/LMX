#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmx.settings')
    os.environ.setdefault('SOCIAL_AUTH_GITHUB_KEY', '98a8e4b3da8efde33d79f15ba61b6c91d6b2256f')
    os.environ.setdefault('SOCIAL_AUTH_GITHUB_SECRET', '98a8e4b3da8efde33d79f15ba61b6c91d6b2256f')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
