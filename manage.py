#!/usr/bin/env python
<<<<<<< HEAD
import os
import sys

if __name__ == '__main__':
=======
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
>>>>>>> d6e74ed4ecdbabd00948f6ec438ca17a54a19a1a
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classroom.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
<<<<<<< HEAD
=======


if __name__ == '__main__':
    main()
>>>>>>> d6e74ed4ecdbabd00948f6ec438ca17a54a19a1a
