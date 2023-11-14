from django.core.management.base import BaseCommand
from os import system

class Command(BaseCommand):
    help = 'Run manage.py test with coverage support'
        #Generate fixtures
                
    def handle(self, *args, **options):
        system("coverage run --omit=testme/reusing/*,../request_casting/reusing/* manage.py test ; coverage html")
