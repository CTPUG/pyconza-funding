from django.contrib import admin

from reversion.admin import VersionAdmin

from pyconza.funding.models import FundingApplication

class FundingApplicationAdmin(VersionAdmin):
    list_display = ('applicant', 'total_cost', 'total_requested', 'status', 'offered')
    list_editable = ('status', 'offered')


admin.site.register(FundingApplication, FundingApplicationAdmin)
