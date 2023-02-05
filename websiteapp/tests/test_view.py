from django.test import TestCase
from django.urls import reverse


class WebsiteViewsTests(TestCase):
    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'website/home.html')
        self.failUnlessEqual(response.status_code, 200)

    def test_404_view(self):
        response = self.client.get('/something/really/weird/')
        self.assertTemplateUsed(response, 'website/404.html')
        self.failUnlessEqual(response.status_code, 404)
