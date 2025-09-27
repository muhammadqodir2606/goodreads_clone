from django.contrib import admin
from .models import Book, BookAuthor, Author, BookReview


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'description')
    search_fields = ('title', 'isbn')


admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor)
admin.site.register(Author)
admin.site.register(BookReview)
