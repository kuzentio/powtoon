from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        permissions = Permission.objects.filter(codename__in=['can_share', 'can_see'])
        powtoon_admin_group = Group.objects.get(name='Powtoon admins')

        for permission in permissions:
            powtoon_admin_group.permissions.add(permission)
