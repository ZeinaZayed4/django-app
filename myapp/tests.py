from django.test import TestCase, override_settings
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

class BookStoreTemplateTests(TestCase):
    def test_home_uses_index_template(self):
        response = self.client.get(reverse("dot:home"))
        self.assertTemplateUsed(response, "myapp/index.html")
        self.assertTemplateUsed(response, "myapp/base.html")

    def test_book_list_uses_list_template_and_shows_all_books(self):
        response = self.client.get(reverse("dot:book_list"))
        self.assertTemplateUsed(response, "myapp/book_list.html")
        self.assertContains(response, "The Little Prince")
        self.assertContains(response, "Eat, Pray, Love")

    def test_book_list_links_use_named_urls(self):
        response = self.client.get(reverse("dot:book_list"))
        self.assertContains(response, reverse("dot:book_detail", kwargs={"id": 2}))

    def test_book_list_truncates_long_descriptions(self):
        response = self.client.get(reverse("dot:book_list"))
        self.assertNotContains(response, "subsequent choices that she made in her life.")

    def test_book_detail_uses_detail_template_and_shows_book(self):
        response = self.client.get(reverse("dot:book_detail", kwargs={"id": 4}))
        self.assertTemplateUsed(response, "myapp/book_detail.html")
        self.assertContains(response, "Pride and Prejudice")
        self.assertEqual(response.context["book"]["id"], 4)

    def test_navigation_comes_from_base_on_every_page(self):
        pages = [
            reverse("dot:home"),
            reverse("dot:book_list"),
            reverse("dot:book_detail", kwargs={"id": 1}),
        ]
        for url in pages:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'class="site-nav"', count=1)
                self.assertContains(response, reverse("dot:book_list"))

    def test_stylesheet_is_linked_on_pages(self):
        response = self.client.get(reverse("dot:home"))
        self.assertContains(response, "myapp/styles.css")


@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver", "localhost"])
class CustomNotFoundTests(TestCase):
    def test_unknown_url_returns_custom_404_page(self):
        missing = reverse("dot:book_list") + "page/"
        response = self.client.get(missing)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "myapp/404.html")
        self.assertContains(response, "Page not found", status_code=404)

    def test_missing_book_also_uses_404_page(self):
        response = self.client.get(reverse("dot:book_detail", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "myapp/404.html")
