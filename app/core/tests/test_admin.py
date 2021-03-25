from django.test import TestCase
from django.contrib.auth import get_user_model
# Helper function called reverse which allows you to generate URLs
# for the Django admin page.
from django.urls import reverse
# Importing the test client that allows you make test requests
# to your application in your unit tests.
from django.test import Client


class AdminSiteTests(TestCase):

    # setup function runs before all of the test functions.
    def setUp(self):
        # sets to self a client variable
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@mail.com",
            password="password123"
        )
        # this uses the client helper function that allows you to
        # log a user in with the Django authentication.
        # it means you don't have to manually log the user in.
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@mail.com",
            password="password123",
            name="Test user full name"
        )

    # check if users are listed in your django admin.
    # this django admin will be slightly modified from the default
    # therefore this is necessary.
    def test_users_listed(self):
        """Test the users are listed on user page"""
        # format 'app:url'
        # core_user_changelist is hardcoded in django;
        # find it in documentation
        url = reverse("admin:core_user_changelist")
        # res = response
        res = self.client.get(url)

        # custom django assertion
        # looks into res and checks for content
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    # test that the change page renders correctly
    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        # checks for status code 200 which means "OK"
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
