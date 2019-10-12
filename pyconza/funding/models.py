from django.db import models
from django.db.models import F, Q

from django.utils.translation import ugettext as _
from django.conf import settings

from wafer.talks.models import (ACCEPTED, SUBMITTED, UNDER_CONSIDERATION,
                                PROVISIONAL)


class FundingApplication(models.Model):
    """A funding application for PyCon ZA"""

    class Meta:
        permissions = (
            ('view_all_applications', _("Can view all funding applications")),
            ('make_application_decisions', _("Can update the application status and make offers")),
        )
        verbose_name = _("funding application")
        verbose_name_plural = _("funding applications")

    STATUS_CHOICES = (
        ('S', _('Submitted')),
        ('U', _('Under Consideration')),
        ('G', _('Request Granted')),
        ('A', _('Offer accepted')),
        ('R', _('Funding not granted')),
        ('N', _('Offer not accepted')),
        ('C', _('Canceled')),
    )

    applicant = models.OneToOneField(settings.AUTH_USER_MODEL,
                                     related_name='funding',
                                     on_delete=models.PROTECT)

    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default='S')

    motivation = models.TextField(blank=True,
                                  help_text=_("Your motivation for why PyCon ZA should fund you"))

    country = models.TextField(blank=True,
                               help_text=_("Which country will you be travelling from?"))
    
    travel_amount = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                        help_text=_("Total Budget for travel (ZAR)"))

    accomodation_amount = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                              help_text=_("Total Budget for accomodation while attending PyCon ZA (ZAR)"))

    food_amount = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                        help_text=_("Total Budget for food while attending PyCon ZA (ZAR)"))

    local_transport_amount = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                                 help_text=_("Total Budget for local transport"
                                                             " expenses while attending"
                                                             " PyCon ZA (ZAR)"))

    other_expenses = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                          help_text=_("Total Budget for other expenses (ZAR)."
                                                      " Please explain these expenses"
                                                      " in your budget description."))

    own_contribution = models.DecimalField(decimal_places=2, default=0, max_digits=10,
                                           help_text=_("Amount you can contribute towards"
                                                       " attending PyCon ZA (ZAR)"))

    # The amount offered - only editable by the admin interface
    offered = models.DecimalField(decimal_places=2, default=0, max_digits=10)

    budget_description = models.TextField(blank=True,
                                          help_text=_("Additional information and explanations"
                                                      " about your budget figures"
                                                      " (assumptions made, special"
                                                      " considerations, etc.)"))

    def sql_total_cost(self):
        """Get the total cost from an sql query for the admin inteface"""
        return (F('food_amount') + F('local_transport_amount') + F('other_expeneses') +
                F('accomodation_amount') + F('travel_amount'))

    sql_total_cost.short_description = _("Total budget")

    def sql_total_requested(self):
        """The total requested as an SQL Query for the admin interface"""
        return self.sql_total_cost() - F('own_contribution')

    sql_total_requested.short_description = _("Total funding requested")

    @property
    def total_cost(self):
        """Total cost as a number, for use elsewhere."""
        # I'm sure this is a terrible way to do this, but it avoids needing to keep
        # multiple lists of fields used to calculate the total in sync
        result = 0
        for expr in self.sql_total_cost().get_source_expressions():
            result += getattr(self, expr.name)
        return result

    @property
    def total_requested(self):
        """Get the total requested as a number, for use elsewhere"""
        return self.total_cost - self.own_contribution

    def can_edit(self, user):
        if user.has_perm('funding.change_application'):
            return True
        # Applicants can only edit the talk while it's in the initial submission state
        if self.status == 'submitted':
            if self.applicant == user:
                return True
        return False

    def has_talk(self):
        """True if the user has submitted a talk that has either been accepted or is
           still being considered."""
        if self.applicant.talks.filter(Q(status=SUBMITTED) |
                                       Q(status=UNDER_CONSIDERATION) |
                                       Q(status=PROVISIONAL) |
                                       Q(status=ACCEPTED)):
            return True
        return False

    has_talk.short_description = _("Has submitted a talk")
    has_talk.boolean = True
