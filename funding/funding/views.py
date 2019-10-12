from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _

from reversion import revisions
from reversion.models import Version

from .models import Application
from wafer.users.models import UserProfile

# Long descriptions of the funding choices for the template
FUNDING_DESCRIPTIONS = {
    'S': _('This funding request has been submitted'),
    'U': _('This request has been finalised and is under consideration by the committee.'),
    'G': _('This funding request has been granted and is waiting for your acceptance'),
    'A': _('This funding offer has been accepted'),
    'R': _('The committee has not granted this funding request')
    'N': _('The funding offer was not accepted'),
    'C': _('This funding request has been canceled'),
}


# Show the offer for these states
SHOW_OFFER = ('G', 'A', 'N')


