from django.contrib import admin

from .models import Author, BookGenre, Book, BookInstance

# Register your models here.


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(BookGenre)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


class BooksInline(admin.TabularInline):
    model = Book


# admin.site.register(BookInstance)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    inlines = [BooksInline]




@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ['title', 'author', 'rate', 'year']
    list_display = ('title', 'display_author', 'year', 'description', 'display_genre')
    exclude = ['release']
    inlines = [BooksInstanceInline]



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ['status', 'due_back']

    fieldsets = (
        ("Book data", {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }

        )

    )


# admin.site.register(Author, AuthorAdmin)
