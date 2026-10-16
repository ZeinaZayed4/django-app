from django.test import TestCase
from django.urls import reverse

class BookStoreViewTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse("dot:home"))
        self.assertEqual(response.status_code, 200)

    def test_book_list_returns_200(self):
        response = self.client.get(reverse("dot:book_list"))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_existing_book_returns_200(self):
        response = self.client.get(reverse("dot:book_detail", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_missing_book_returns_404(self):
        response = self.client.get(reverse("dot:book_detail", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_old_catalog_redirects_to_book_list(self):
        response = self.client.get(reverse("dot:old_catalog"))
        self.assertRedirects(response, reverse("dot:book_list"))
