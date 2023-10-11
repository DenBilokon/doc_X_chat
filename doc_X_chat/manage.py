#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    The main function is used to run administrative tasks.
    
    :return: The value returned by the execute_from_command_line() function
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doc_X_chat.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Couldn't import Django.")
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
