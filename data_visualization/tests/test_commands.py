from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from data_visualization.models import DataItem, Region

User = get_user_model()


class UploadDataTest(TestCase):
    def test_upload_data(self):
        call_command('upload_data', 'data/input_data.csv')
        self.assertEqual(DataItem.objects.count(), 583)
