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
