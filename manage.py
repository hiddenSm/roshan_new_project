#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# Set the Twisted reactor before importing any Django settings
try:
    from twisted.internet import asyncioreactor
    asyncioreactor.install()
except Exception as e:
    print(f"Reactor already installed: {e}")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshan_news.settings')
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
