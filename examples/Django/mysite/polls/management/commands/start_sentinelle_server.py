import os
import sys
import unittest

from django.conf import settings
from django.core.management.base import BaseCommand
from django.test.utils import get_runner


SENTINELLE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "..", "..", "..")
sys.path.insert(0, os.path.join(SENTINELLE_PATH))


import sentinelle  # noqa: E402


# TODO: logging!!!
class Command(BaseCommand):
    help = 'Start a Sentinelle Test Server'

    def handle(self, *args, **options):
        unittest.installHandler()

        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
        inspector = sentinelle.inspectors.DjangoTestingInspector()

        try:
            sentinelle.serve(avec=inspector)
        except Exception as e:
            import traceback
            print('hoge', e)
            print(traceback.format_exc())
        finally:
            unittest.removeHandler()
