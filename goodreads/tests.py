from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Deep work", description="Description 1", isbn=11111, price=1)
        self.user = CustomUser.objects.create(
            username="muhammadqodir", first_name="Muhammadqodir", last_name="Jalilov", email='jalilovm54@gmail.com'
        )
        self.user.set_password("somepass")
        self.user.save()

    def test_paginated_list(self):
        review1 = BookReview.objects.create(book=self.book, user=self.user, stars_given=3, comment="Very good book")
        review2 = BookReview.objects.create(book=self.book, user=self.user, stars_given=4, comment="Useful book")
        review3 = BookReview.objects.create(book=self.book, user=self.user, stars_given=5, comment="Nice book")

        response = self.client.get(reverse('home_page') + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
