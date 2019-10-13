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
from crispy_forms.layout import Submit, HTML
from easy_select2.widgets import Select2Multiple
from markitup.widgets import MarkItUpWidget

from .models import FundingApplication


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

