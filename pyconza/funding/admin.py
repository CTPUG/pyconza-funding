from django.contrib import admin
from django.utils.translation import ugettext as _

from wafer.compare.admin import CompareVersionAdmin

from pyconza.funding.models import FundingApplication
from pyconza.funding.views import FUNDING_DESCRIPTIONS


def check_app_status(all_applications):
    """Check that the application status is sane -
       Granted and so forth applications have offers, applications still
       under review don't, and so forth"""
    errors = []
    for application in all_applications:
        if application.offered > 0:
            if application.status not in ['G', 'A', 'N']:
                errors.append(
                    (application,
                     _('Application has an offer, but is in the incorrect state.'
                       'Current state: %s') % FUNDING_DESCRIPTIONS[application.status]))
        else:
            if application.status in ['G', 'A', 'N']:
                errors.append((application,
                               _("Application should have an offered figure, but doesn't")))
    return errors


def calc_totals(all_applications):
    totals = {
        'total': 0,
        'not_accepted': 0,
        'accepted': 0,
        'not_decided': 0,
        'total_cost': 0,
    }
    for app in all_applications:
        totals['total'] += app.offered
        if app.status == 'N':
            totals['not_accepted'] += app.offered
        elif app.status == 'A':
            totals['accepted'] += app.offered

    # Inferred values
    totals['not_decided'] = totals['total'] - totals['accepted']  - totals['not_accepted']
    totals['total_cost'] = totals['accepted'] + totals['not_decided']
    return totals


VALIDATORS = [check_app_status]


class FundingApplicationAdmin(CompareVersionAdmin):
    list_display = ('get_user_fullname', 'total_cost', 'total_requested', 'has_talk', 'status', 'offered')
    list_editable = ('status', 'offered')
    list_filter= ('status',)

    change_list_template = 'admin/funding_admin_list.html'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        all_applications = FundingApplication.objects.all()
        wrong_applications = []
        # Check for any consistent status
        for validator in VALIDATORS:
            # Validators return a list of (app, msg) tuples
            wrong_applications.extend(validator(all_applications))
        wrong_applications.sort(key=lambda x: x[0].pk)
        extra_context['errors'] = wrong_applications
        # Calculate relevant totals
        extra_context['totals'] = calc_totals(all_applications)
        return super(FundingApplicationAdmin, self).changelist_view(request,
                                                                    extra_context)


admin.site.register(FundingApplication, FundingApplicationAdmin)
