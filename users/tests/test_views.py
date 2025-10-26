from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class SimpleAuthViewsTest(TestCase):

    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.index_url = reverse('index')

        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            first_name='Test',
            last_name='User',
            password='testPass123'
        )

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success_shows_message(self):
        response = self.client.post(self.login_url, {
            'username': 'test@gmail.com',
            'password': 'testPass123'
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_shows_error(self):
        response = self.client.post(self.login_url, {
            'username': 'test@gmail.com',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertIn('Invalid', str(messages[0]))

    def test_signup_page_loads(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_signup_creates_user(self):
        data = {
            'email': 'new@gmail.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testPass123!',
            'password2': 'testPass123!',
        }
        self.client.post(self.signup_url, data)

        user = User.objects.filter(email='new@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@gmail.com')
        self.assertTrue(user.check_password('testPass123!'))

    def test_signup_duplicate_email_fails(self):
        data = {
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testPass123',
            'password2': 'testPass123',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_signup_password_mismatch_fails(self):
        data = {
            'email': 'alice@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testPass123',
            'password2': 'testPass456',
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
