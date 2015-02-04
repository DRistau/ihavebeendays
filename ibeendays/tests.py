from django.test import TestCase
from django.core.urlresolvers import reverse


class HomeAvailableTestCase(TestCase):
    def setUp(self):
        self.route = reverse('home')

    def test_home_should_be_available(self):
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 200)
