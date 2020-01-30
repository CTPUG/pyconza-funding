"""Tests for pyconza-funding views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from wafer.tests.api_utils import SortedResultsClient
from wafer.talks.models import (
    Talk, TalkUrl, ACCEPTED, REJECTED, SUBMITTED, UNDER_CONSIDERATION,
    CANCELLED, PROVISIONAL)


def create_user_with_funding(username, superuser=False, perms=()):
    pass


class FundingViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_not_logged_in(self):
        """Test that unauthenticated users can't see anything"""

    def test_admin_user(self):
        """Test that admin users see all applications."""

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

