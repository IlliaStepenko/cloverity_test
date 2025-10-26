from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class IndexViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test@gmail.com',
            email='test@gmail.com',
            password='testpass123'
        )
        self.url = reverse('index')

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/users/login/', response.url)

    def test_page_loads(self):
        self.client.login(email='test@gmail.com', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_data_in_context(self):
        call_command('upload_data', 'data/input_data.csv')
        self.client.login(email='test@gmail.com', password='testpass123')
        response = self.client.get(self.url)
        data = response.context['data']
        self.assertEqual(len(data), 583)
