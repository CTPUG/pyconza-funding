"""Tests for pyconza-funding views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from wafer.tests.api_utils import SortedResultsClient

from pyconza.funding.models import FundingApplication

def create_user(username, superuser=False, perms=()):
    if superuser:
        create = get_user_model().objects.create_superuser
    else:
        create = get_user_model().objects.create_user
    user = create(
        username, '%s@example.com' % username, '%s_password' % username)
    for codename in perms:
        perm = Permission.objects.get(codename=codename)
        user.user_permissions.add(perm)
    if perms:
        user = get_user_model().objects.get(pk=user.pk)
    return user

def create_application(user, status):
    """Create an application with the given status"""
    application = FundingApplication.objects.create(applicant=user)
    application.status = status
    application.save()
    return application


@override_settings(
    ROOT_URLCONF='pyconza.funding.tests.urls',
)
class FundingViewTests(TestCase):
    def setUp(self):
        self.test_user = create_user('test', False)
        self.perm_user = create_user('perm_user', False, ())
        self.admin_user = create_user('admin', True)
        self.no_app_user = create_user('no application', False)
        self.def_app = create_application(self.test_user, 'U')
        self.client = Client()

    def test_not_logged_in(self):
        """Test that unauthenticated users can't see anything"""
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.status_code, 403)

    def test_admin_user(self):
        """Test that admin users see all applications."""
        self.client.login(username='admin', password='admin_password')
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.status_code, 200)

    def test_user_with_view_all(self):
        """Test that users with the view_all permission see all applications."""

    def test_user_view_self(self):
        """Test that a user can see their own application"""

    def test_own_submitted(self):
        """Test that a user can edit / withdraw their application while its submitted"""

    def test_own_under_consideration(self):
        """Test that a user cannot edi or withdraw their application once it's 'Under Consideration'"""

    def test_own_granted(self):
        """Test that a user cannot edit or withdraw their application once it's been granted"""

    def test_own_accepted(self):
        """Test that a user cannot edit or withdraw their application once it's been accepted"""

    def test_own_rejected(self):
        """Test that a user cannot edit or withdraw their application once it's been rejected"""

    def test_accept_reject_option(self):
        """Test that the accept / reject option is displayed after a request has been granted."""
        # Test submitted state
        # Test under consideration state
        # Test granted state
        # Test accepted state
        # Test rejected state

    def test_accept_grant(self):
        """Test that accepting a grant works"""

    def test_reject_grant(self):
        """Test that rejecting a grant works"""

