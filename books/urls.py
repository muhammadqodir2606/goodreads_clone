from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, CreateBookReview, UpdateReviewView, DeleteReviewView, ConfirmDeleteReviewView

app_name = 'books'
urlpatterns = [
    path("", BookListView.as_view(), name='list'),
    path("<int:id>", BookDetailView.as_view(), name='detail'),
    path("create/", BookCreateView.as_view(), name='create'),
    path("<int:id>/reviews/", CreateBookReview.as_view(), name='reviews'),
    path("<int:book_id>/reviews/<int:review_id>", UpdateReviewView.as_view(), name='review-update'),
    path("<int:book_id>/reviews/<int:review_id>/confirm/delete", ConfirmDeleteReviewView.as_view(), name='review-confirm-delete'),
    path('<int:book_id>/reviews/<int:review_id>/delete', DeleteReviewView.as_view(), name='review-delete'),
]
