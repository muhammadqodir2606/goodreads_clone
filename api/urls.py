from django.urls import path

from api.views import BookReviewDetailView

app_name = 'api'
urlpatterns = [
    path('review/<int:id>/', BookReviewDetailView.as_view(), name='review-detail'),
]