from django.core.management import BaseCommand

from market.celery.base import CeleryRequeue


class Command(BaseCommand):

    def handle(self, *args, **options):
        CeleryRequeue().requeue()
        self.stdout.write('Requeue Run Successfully')

