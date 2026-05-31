from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class LoginViewTests(TestCase):
    """Tests for the login view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
        )

    def test_login_page_loads(self):
        """GET /login/ should return 200."""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_redirect_when_authenticated(self):
        """Authenticated user accessing /login/ should still get 200 (no redirect from login page itself)."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class PublicViewTests(TestCase):
    """Tests for publicly accessible views."""

    def test_faq_page_loads(self):
        """GET /FAQ/ should return 200 for unauthenticated users."""
        response = self.client.get('/FAQ/')
        self.assertEqual(response.status_code, 200)

    def test_formshd_page_loads(self):
        """GET /formshd/ should return 200 for unauthenticated users."""
        response = self.client.get('/formshd/')
        self.assertEqual(response.status_code, 200)


class AuthenticatedViewTests(TestCase):
    """Tests for views that require authentication."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='staffuser',
            password='staffpassword123',
        )
        self.client.login(username='staffuser', password='staffpassword123')

    def test_home_requires_login(self):
        """Unauthenticated access to /home/ should redirect to /login/."""
        unauthenticated_client = Client()
        response = unauthenticated_client.get('/home/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_home_page_loads_for_authenticated_user(self):
        """Authenticated user should get 200 on /home/."""
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
