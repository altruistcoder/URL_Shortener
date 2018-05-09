from django.core.management.base import BaseCommand, CommandError

from shortish.models import ShortishURL


class Command(BaseCommand):
    help = 'Refreshes all Shortish shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)    # -- makes argument items optional instead of required

    def handle(self, *args, **options):
        return ShortishURL.objects.refresh_shortcodes(items=options['items'])
