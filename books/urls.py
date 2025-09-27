from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, CreateBookReview

app_name = 'books'
urlpatterns = [
    path("", BookListView.as_view(), name='list'),
    path("<int:id>", BookDetailView.as_view(), name='detail'),
    path("create/", BookCreateView.as_view(), name='create'),
    path("<int:id>/reviews/", CreateBookReview.as_view(), name='reviews')
]