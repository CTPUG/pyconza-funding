from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _

from reversion import revisions
from reversion.models import Version

from wafer.users.models import UserProfile

from .models import FundingApplication
from .forms import FundingApplicationForm

# Long descriptions of the funding choices for the template
FUNDING_DESCRIPTIONS = {
    'S': _('This funding request has been submitted'),
    'U': _('This request has been finalised and is under consideration by the committee.'),
    'G': _('This funding request has been granted and is waiting for your decision on accepting the offer'),
    'A': _('This funding offer has been accepted'),
    'R': _('The committee has not granted this funding request'),
    'N': _('The funding offer was not accepted'),
    'C': _('This funding request has been canceled'),
}


# Show the offer for these states
SHOW_OFFER = ('G', 'A', 'N')

class EditOwnApplicationMixin(object):
    """Users can edit their own application long as it is in the 'Submitted' state"""
    def get_object(self, *args, **kwargs):
        object_ = super(EditOwnApplicationMixin, self).get_object(*args, **kwargs)
        if object_.can_edit(self.request.user):
            return object_
        else:
            raise PermissionDenied


class FundingApplicationView(DetailView):
    template_name = 'pyconza.funding/application.html'
    model = FundingApplication

    def get_object(self, *args, **kwargs):
        '''Only owners and funding committee can see applications'''
        object_ = super(FundingApplicationView, self).get_object(*args, **kwargs)
        if not object_.can_view(self.request.user):
            raise PermissionDenied
        return object_

    def get_context_data(self, **kwargs):
        context = super(FundingApplicationView, self).get_context_data(**kwargs)
        application = self.object
        user = self.request.user

        context['show_offer'] = application.status in SHOW_OFFER
        context['status_description'] = FUNDING_DESCRIPTIONS[application.status]
        context['can_edit'] = application.can_edit(user)

        return context


class FundingApplicationCreate(LoginRequiredMixin, CreateView):
    model = FundingApplication
    template_name = 'pyconza.funding/application_form.html'
    form_class = FundingApplicationForm

    def get_context_data(self, **kwargs):
        context = super(FundingApplicationCreate, self).get_context_data(**kwargs)

        context['can_edit'] = True
        context['can_submit'] = True

        return context

    @revisions.create_revision()
    def form_valid(self, form):
        # Eaaargh we have to do the work of CreateView if we want to set values
        # before saving
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        revisions.set_user(self.request.user)
        revisions.set_comment("Funding Application Created")
        return HttpResponseRedirect(self.get_success_url())


class FundingApplicationUpdate(EditOwnApplicationMixin, UpdateView):
    model = FundingApplication
    template_name = 'pyconza.funding/application_form.html'
    form_class = FundingApplicationForm

    def get_context_data(self, **kwargs):
        context = super(FundingApplicationUpdate, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_edit(self.request.user)
        return context

    @revisions.create_revision()
    def form_valid(self, form):
        revisions.set_user(self.request.user)
        revisions.set_comment("Funding Application Modified")
        return super(FundingApplicationUpdate, self).form_valid(form)


class FundingApplicationCancel(EditOwnApplicationMixin, DeleteView):
    model = FundingApplication
    template_name = 'pyconza.funding/cancel_application.html'
    success_url = reverse_lazy('wafer_page')

    @revisions.create_revision()
    def delete(self, request, *args, **kwargs):
        """Override delete to only cancel"""
        application = self.get_object()
        application.status = 'C'
        application.save()
        revisions.set_user(self.request.user)
        revisions.set_comment("Funding Application Cancelled")
        return HttpResponseRedirect(self.success_url)
