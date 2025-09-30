from django.test import TestCase
from django.urls import reverse

<<<<<<< HEAD
from books.models import Book, BookReview
=======
from books.models import Book, BookAuthor, Author
>>>>>>> 01cd144 (Men books detailga authors ni ham qo'shdim va test yozdim, yana review qoldirish va reviews listga yulduzchali tanlash qo'shdim)
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(
            reverse("books:list")
        )
        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book 1", description="Description 1", isbn=11111, price=1)
        book2 = Book.objects.create(title="Book 2", description="Description 2", isbn=22222, price=2)
        book3 = Book.objects.create(title="Book 3", description="Description 3", isbn=33333, price=3)

        response = self.client.get(reverse("books:list") + "?page_size=2")
        for book in [book3, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book1.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book 1", description="Description 1", isbn=11111, price=1)

        response = self.client.get(
            reverse("books:detail", kwargs={"id": book.id})
        )
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, str(book.isbn))
        self.assertContains(response, str(book.price))

    def test_books_search(self):
        book1 = Book.objects.create(title="Atomic habits", description="Description 1", isbn=11111, price=1)
        book2 = Book.objects.create(title="Diqqat", description="Deep work's description 2", isbn=22222, price=2)
        book3 = Book.objects.create(title="Steve Jobs", description="Description 3", isbn=33333, price=3)

        response = self.client.get(reverse("books:list") + "?q=Atomic habits")

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Deep work")

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Steve")

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)


class BookReviewTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Deep work", description="Description 1", isbn=11111, price=1)
        self.user = CustomUser.objects.create(
            username="muhammadqodir", first_name="Muhammadqodir", last_name="Jalilov", email='jalilovm54@gmail.com'
        )
        self.user.set_password("somepass")
        self.user.save()

    def test_add_review(self):
        self.client.login(username="muhammadqodir", password='somepass')
        self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'stars_given': 3,
                'comment': 'Nice book',
                'book': self.book
            }
        )
        self.book.refresh_from_db()
        book_reviews = self.book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, self.book)
        self.assertEqual(book_reviews[0].user, self.user)

    def test_required_fields(self):
        self.client.login(username="muhammadqodir", password='somepass')
        response = self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'book': self.book
            }
        )
        self.book.refresh_from_db()
        form = response.context['review_form']
        self.assertFormError(form, 'stars_given', 'This field is required.')
        self.assertFormError(form, 'comment', 'This field is required.')

    def test_stars_given_value_limit(self):
        self.client.login(username="muhammadqodir", password='somepass')
        response = self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'stars_given': 8,
                'comment': 'Nice book',
                'book': self.book
            }
        )

        form = response.context['review_form']
        self.assertFormError(form, 'stars_given', 'Ensure this value is less than or equal to 5.')

        response = self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'stars_given': 0,
                'comment': 'Nice book',
                'book': self.book
            }
        )

        form = response.context['review_form']
        self.assertFormError(form, 'stars_given', 'Ensure this value is greater than or equal to 1.')

    def test_login_required(self):
        response = self.client.post(
            reverse('books:reviews', kwargs={'id': self.book.id}),
            data={
                'stars_given': 8,
                'comment': 'Nice book',
                'book': self.book
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login') + f"?next=/books/{self.book.id}/reviews/")


class BookAuthorTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title="Deep work", description="Description 1", isbn=11111, price=1)
        self.author1 = Author.objects.create(first_name="John", last_name="Doe", email="john@gmail.com", bio="John was born in 2000")
        self.author2 = Author.objects.create(first_name="Mukhammadkodir", last_name="Jalilov", email="mukh@gmail.com", bio="Mukhammadkodir was born in 2005")
        self.book_author = BookAuthor.objects.create(author=self.author1, book=self.book)
        self.book_author = BookAuthor.objects.create(author=self.author2, book=self.book)

    def test_book_author(self):
        response = self.client.get(reverse('books:detail', kwargs={'id': self.book.id}))
        self.assertContains(response, self.author1.first_name)
        self.assertContains(response, self.author1.last_name)
        self.assertContains(response, self.author2.first_name)
        self.assertContains(response, self.author2.last_name)
