from django import forms
from books.models import Book, BookReview


class BookCreateForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)
    isbn = forms.IntegerField()
    price = forms.DecimalField(max_digits=10, decimal_places=2)

    def save(self):
        book = Book.objects.create(
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            isbn=self.cleaned_data['isbn'],
            price=self.cleaned_data['price']
        )
        return book


class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ['comment', 'stars_given']
