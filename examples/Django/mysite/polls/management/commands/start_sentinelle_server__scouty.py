import os
import sys
import unittest

from django.core.management.base import BaseCommand


SENTINELLE_PATH = '/sentinelle/sentinelle'
sys.path.insert(0, os.path.join(SENTINELLE_PATH))


import sentinelle  # noqa: E402


class Command(BaseCommand):
    help = 'Start a Sentinelle Test Server'

    def handle(self, *args, **options):
        unittest.installHandler()

        os.environ['DJANGO_SETTINGS_MODULE'] = \
            'application.sc_tests.settings.test_settings'
        inspector = sentinelle.inspectors.DjangoTestingInspector()

        try:
            sentinelle.serve(avec=inspector)
        except Exception as e:
            import traceback
            print('hoge', e)
            print(traceback.format_exc())
        finally:
            unittest.removeHandler()
