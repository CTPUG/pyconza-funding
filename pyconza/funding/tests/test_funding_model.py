# This tests the very basic funding stuff, to ensure some levels of sanity


from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from pyconza.funding.models import FundingApplication

def create_user(name):
    user = get_user_model().objects.create_user(name, '%s@wafer.test' % name,
                                                'password')
    return user

class FundingTests(TestCase):

    def test_add_application(self):
        """Create a user and add a application for it"""

        user = create_user('john')

        with self.assertRaises(AttributeError) as cm:
            s = user.funding_application

        self.assertTrue("has no funding_application" in str(cm.exception))

        application = FundingApplication.objects.create(
            applicant=user)

        self.assertTrue(user.funding_application is not None)
        self.assertTrue(user.funding_application is application)
        self.assertTrue(application.applicant is user)

    def test_total_cost(self):
        """Test that the total cost is updated correctly"""
        user = create_user('james')

        application = FundingApplication.objects.create(
            applicant=user)

        self.assertEqual(application.total_cost, 0)
        application.other_expenses = 1
        application.save()
        self.assertEqual(application.total_cost, 1)

        application.food_amount = 2
        application.local_transport_amount = 2
        application.save()
        self.assertEqual(application.total_cost, 5)
        application.local_transport_amount = 3
        application.save()
        self.assertEqual(application.total_cost, 6)

        application.travel_amount = 10
        application.save()
        self.assertEqual(application.total_cost, 16)
        application.travel_amount = 5
        application.save()
        self.assertEqual(application.total_cost, 11)

        application.accomodation_amount = 1
        application.save()
        self.assertEqual(application.total_cost, 12)

    def test_total_requested(self):
        """Test that the total requested is updated correctly."""
