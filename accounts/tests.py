from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.username = 'testuser'
        self.password = 'TestPass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
        )

    def test_signup_page_renders(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(
            self.signup_url,
            {
                'username': 'newuser',
                'password1': 'NewPass123',
                'password2': 'NewPass123',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.url, self.login_url)

    def test_login_and_logout_flow(self):
        response = self.client.post(
            self.login_url,
            {'username': self.username, 'password': self.password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.session.get('_auth_user_id'))

        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
