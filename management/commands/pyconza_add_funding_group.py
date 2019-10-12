from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from django.utils.translation import ugettext as _

class Command(BaseCommand):

    help = _("Add a group with permission to manage funding applications")

    def add_funding_group(self):
        group_name = "Funding Group"
        group_perms = (('funding', 'add_application'),
                       ('funding', 'view_all_applications'))
                       ('funding', 'change_application'))

        group, created = Group.objects.all().get_or_create(name=group_name)
        if not created:
            print(_("Using exisitng %s group") % group_name)

        for app, perm_code in group_perms:
            try:
                perm = Permission.objects.filter(
                    codename=perm_code, content_type__app_label=app).get()
            except Permission.DoesNotExist:
                print(_('Unable to find permission %s') % perm_code)
                continue
            except Permission.MultipleObjectsReturned:
                print(_('Non-unique permission %s') % perm_code)
                continue
            if perm not in group.permissions.all():
                print(_('Adding %s to %s') % (perm_code, group_name))
                group.permissions.add(perm)
        group.save()

    def handle(self, *args, *options):
        self.add_funding_group()

