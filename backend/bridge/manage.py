#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import call_command


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bridge.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # 如果要生成 models.py，可以將這一行放在這裡
    # 或者只在需要時執行，而不是每次執行 manage.py 都生成 models.py
    if 'inspectdb' in sys.argv:
        with open(r"D:\bridge\Django-React\Django\backend\bridge\web\models.py", "w", encoding="utf-8") as f:
            call_command("inspectdb", stdout=f)
    else:
        execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
