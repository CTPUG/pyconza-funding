import copy

from django import forms
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, HTML
from easy_select2.widgets import Select2Multiple
from markitup.widgets import MarkItUpWidget

from .models import FundingApplication

BUDGET_CLASS = "budget"
REQUEST_CLASS = "request"

class FundingApplicationForm(forms.ModelForm):

    class Meta:
        model = FundingApplication
        fields = ('motivation', 'country', 'travel_amount', 'accomodation_amount',
                  'food_amount', 'local_transport_amount', 'other_expenses',
                  'budget_description', 'own_contribution')
        widgets = {
            'motivation': forms.Textarea(attrs={'class': 'input-xxlarge'}),
            'budget_description': forms.Textarea(attrs={'class': 'input-xxlarge'}),
        }

    def __init__(self, *args, **kwargs):
        super(FundingApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.include_media = False
        # We group the budget items together, and add a css class so we can use
        # javascript for the total
        # Likewise, we add a css_class to the own_contribution field for javascript
        # calculation of the total_requested
        self.helper.layout = Layout(
            'motivation'
            'country',
            Fieldset(
                'Your budget',
                Field('travel_amount', css_class=BUDGET_CLASS, onblur="updateTotal()"),
                Field('accomodation_amount', css_class=BUDGET_CLASS, onblur="updateTotal()"),
                Field('food_amount', css_class=BUDGET_CLASS, onblur="updateTotal()"),
                Field('local_transport_amount', css_class=BUDGET_CLASS, onblur="updateTotal()"),
                Field('other_expenses', css_class=BUDGET_CLASS, onblur="updateTotal()"),
                HTML('<p>Total Budget: <strong class="%s_total">R </strong></p>' % BUDGET_CLASS),
                'budget_description',
            ),
            Field('own_contribution', css_class=REQUEST_CLASS, onblur="updateRequestedTotal()"),
            HTML('<p>Total Requested: <strong class="%s_total">R </strong></p>' % REQUEST_CLASS),
        )
        instance = kwargs['instance']
        submit_button = Submit('submit', _('Save') if instance else _('Submit'))
        if instance:
            self.helper.layout.append(
                FormActions(
                    submit_button,
                    HTML('<a href="%s" class="btn btn-danger">%s</a>'
                         % (reverse('pyconza_funding_withdraw', args=(instance.pk,)),
                            _('Withdraw Application')))))
        else:
            self.helper.add_input(submit_button)

