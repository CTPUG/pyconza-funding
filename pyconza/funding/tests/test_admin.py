"""Tests for pyconza-funding admin interface."""
from django.test import TestCase, override_settings

from pyconza.funding.models import FundingApplication
from pyconza.funding.admin import check_app_status
from pyconza.funding.tests.test_view import create_user, create_application

@override_settings(
    ROOT_URLCONF='pyconza.funding.tests.urls',
)
class FundingAdminTests(TestCase):
    def setUp(self):
        self.test_user = create_user('test', False)
        self.def_app = create_application(self.test_user, 'U')

    def test_validation_no_offers(self):
        """Check the various validation cases with no offers."""
        # Submitted
        self.assertEqual(check_app_status(FundingApplication.objects.all()), [])
        # Under consideration
        self.def_app.status = 'U'
        self.def_app.save()
        self.assertEqual(check_app_status(FundingApplication.objects.all()), [])
        # Final Review
        self.def_app.status = 'F'
        self.def_app.save()
        self.assertEqual(check_app_status(FundingApplication.objects.all()), [])
        # Not granted
        self.def_app.status = 'R'
        self.def_app.save()
        self.assertEqual(check_app_status(FundingApplication.objects.all()), [])
        # Cancelled
        self.def_app.status = 'C'
        self.def_app.save()
        self.assertEqual(check_app_status(FundingApplication.objects.all()), [])
        # Check failures
        # Granted
        self.def_app.status = 'G'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Rejected offer
        self.def_app.status = 'N'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Accepted offer
        self.def_app.status = 'A'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)

    def test_validation_offer(self):
        """Test validation erros with an offer."""
        self.def_app.offered = 1000.00
        self.def_app.save()
        # Submitted
        self.def_app.status = 'S'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Under Consideration
        self.def_app.status = 'U'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Final Review
        self.def_app.status = 'F'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Not granted
        self.def_app.status = 'R'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Cancelled
        self.def_app.status = 'C'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0][0], self.def_app)
        # Check successes
        # Granted
        self.def_app.status = 'G'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 0)
        # Rejected
        self.def_app.status = 'N'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 0)
        # Accepted
        self.def_app.status = 'A'
        self.def_app.save()
        errors = check_app_status(FundingApplication.objects.all())
        self.assertEqual(len(errors), 0)

