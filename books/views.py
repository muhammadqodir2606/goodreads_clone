from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Book, BookReview
from .forms import BookCreateForm, BookReviewForm


class BookListView(View):
    def get(self, request):
        search_query = request.GET.get('q', '')
        books = Book.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query)).order_by('-id')
        page_size = request.GET.get('page_size', 4)
        page_num = request.GET.get('page', 1)
        paginator = Paginator(books, page_size)
        page_obj = paginator.get_page(page_num)
        return render(
            request,
            'books/list.html',
            {'page_obj': page_obj, 'search_query': search_query}
        )


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        book_reviews = book.bookreview_set.all().order_by('-created_at')
        review_form = BookReviewForm()
        return render(
            request,
            "books/detail.html",
            {
                "book": book,
                'review_form': review_form,
                'book_reviews': book_reviews
             }
        )


class BookCreateView(View):
    def get(self, request):
        form = BookCreateForm()
        return render(request, "books/create.html", {"form": form})

    def post(self, request):
        form = BookCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("books:list")
        else:
            return render(request, "books/create.html", {"form": form})


class BookUpdateView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        BookCreateForm(instance=book)


class CreateBookReview(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)
        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        else:
            return render(
                request,
                "books/detail.html",
                {
                    'book': book,
                    "review_form": review_form
                }
            )


class UpdateReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/edit_review.html', {'book': book, 'review': review, 'review_form': review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        return render(
            request,
            'books/confirm_delete_review.html',
            {'book': book, 'review': review, 'review_form': review_form})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        review = BookReview.objects.get(id=review_id)
        if review.user == request.user:
            review.delete()
            messages.success(request, 'Review successfully deleted.')
            return redirect(reverse('books:detail', kwargs={'id': book_id}))
