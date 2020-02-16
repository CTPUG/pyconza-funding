"""Tests for pyconza-funding views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase, override_settings
from django.utils.http import urlencode
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
        perm = Permission.objects.get(codename='view_all_applications')
        self.perm_user.user_permissions.add(perm)
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
        self.client.login(username='perm_user', password='perm_user_password')
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.status_code, 200)

    def test_user_view_self(self):
        """Test that a user can see their own application"""
        self.client.login(username='test', password='test_password')
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.status_code, 200)

    def test_own_submitted(self):
        """Test that a user can edit / withdraw their application while it's
           submitted, but cannot accept it"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'S'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], True)
        self.assertEqual(response.context_data['can_accept'], False)

    def test_own_under_consideration(self):
        """Test that a user can edit / withdraw their application while it's
           under consideratoon, but cannot accept it"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'U'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], True)
        self.assertEqual(response.context_data['can_accept'], False)

    def test_own_final_review(self):
        """Test that a user cannot edit, withdraw or accept / rehect their application
           once it's 'Final Review'"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'F'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], False)
        self.assertEqual(response.context_data['can_accept'], False)

    def test_own_granted(self):
        """Test that a user cannot edit or withdraw their application once it's been granted,
           but can accept it"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'G'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], False)
        self.assertEqual(response.context_data['can_accept'], True)

    def test_own_accepted(self):
        """Test that a user cannot edit, withdraw or accept / rehect their application
           been accepted"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'A'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], False)
        self.assertEqual(response.context_data['can_accept'], False)

    def test_own_rejected(self):
        """Test that a user cannot edit, withdraw or accept/reject their application
           once it's been rejected"""
        self.client.login(username='test', password='test_password')
        self.def_app.status = 'N'
        self.def_app.save()
        response = self.client.get('/funding/%d/' % self.def_app.pk)
        self.assertEqual(response.context_data['can_edit'], False)
        self.assertEqual(response.context_data['can_accept'], False)


@override_settings(
    ROOT_URLCONF='pyconza.funding.tests.urls',
)
class FundingE2ETest(TestCase):

    def test_e2e(self):
        """Test the complete flow"""
        test_user = create_user('test', False)
        client = Client()
        form_data = {'travel_amount': 100.00,
                     'accomodation_amount': 100.00,
                     'food_amount': 50.00,
                     'other_expenses': 0.00,
                     'local_transport_amount': 0.00,
                     'budget_description': 'Stuff',
                     'motivation': 'Motivated',
                     'country': 'Far, far away',
                     'own_contribution': 50.00}

        # Submit the application
        client.login(username='test', password='test_password')
        response = client.post('/funding/new/', form_data, follow=True)
        # Successful form redirects us to the application
        self.assertTrue(test_user.funding_application is not None)
        application = test_user.funding_application
        funding_url = '/funding/%d/' % application.pk
        self.assertTrue(funding_url in response.redirect_chain[0][0])
        self.assertEqual(application.total_cost(), 250)
        self.assertEqual(application.total_requested(), 200)
        # Edit form
        form_data['own_contribution'] = 75.00
        client.post(funding_url + 'edit/', form_data, follow=True)
        application.refresh_from_db()
        self.assertEqual(application.total_cost(), 250)
        self.assertEqual(application.total_requested(), 175)
        # Assert that trying to accept fails
        response = client.post(funding_url + 'accept/')
        self.assertEqual(response.status_code, 403)
        # Likewise reject
        response = client.post(funding_url + 'reject/')
        self.assertEqual(response.status_code, 403)
        # Add a grant
        application.status = 'G'
        application.offered = 150.00
        application.save()
        # Test that cancel does nothing
        response = client.post(funding_url + 'reject/', {'cancel': 'cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertTrue(application.status, 'G')
        response = client.post(funding_url + 'accept/', {'cancel': 'cancel'}, follow=True)
        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertTrue(application.status, 'G')
        response = client.post(funding_url + 'accept/', follow=True)
        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.status, 'A')
        response = client.post(funding_url + 'reject/')
        self.assertEqual(response.status_code, 403)
        # Go back in time and test reject
        application.status = 'G'
        application.save()
        response = client.post(funding_url + 'reject/', follow=True)
        self.assertEqual(response.status_code, 200)
        application.refresh_from_db()
        self.assertEqual(application.status, 'N')
        response = client.post(funding_url + 'accept/')
        self.assertEqual(response.status_code, 403)
