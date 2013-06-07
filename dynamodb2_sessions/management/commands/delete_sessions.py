from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Remove all sessions data from relational database'
    
    def handle(self, *args, **options):
        Session.objects.all().delete()
        self.stdout.write('Done!!\n')