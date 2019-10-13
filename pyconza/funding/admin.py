from django.contrib import admin

from reversion.admin import VersionAdmin

from pyconza.funding.models import FundingApplication

class FundingApplicationAdmin(VersionAdmin):
    list_display = ('get_user_fullname', 'total_cost', 'total_requested', 'has_talk', 'status', 'offered')
    list_editable = ('status', 'offered')


admin.site.register(FundingApplication, FundingApplicationAdmin)
