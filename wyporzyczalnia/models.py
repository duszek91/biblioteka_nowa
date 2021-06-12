import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=64, blank=False, unique=True)
    author = models.ForeignKey('Author', max_length=32, blank=False, null=True, on_delete=models.SET_NULL)
    year = models.PositiveSmallIntegerField(default=2000)
    description = models.TextField(default="")
    release = models.DateField(null=True, blank=True)
    rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="okładki", null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, null=True)
    bookgenre = models.ManyToManyField('BookGenre')

    def __str__(self):
        return self.title_with_author()

    def title_with_author(self):
        return f"{self.title} ({self.author})"

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.bookgenre.all()[:3])

    display_genre.short_description = 'Genre'
    def display_author(self):
        return f"{self.author.first_name} {self.author.last_name}"



class BookGenre(models.Model):
    name = models.CharField(max_length=100, help_text="Podaj typ książki (drama, horror etc)")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    due_back = models.DateField(null=True, blank=True)
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=100)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ACTUAL_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
        ('u', 'Unknown'),
    )
    status = models.CharField(max_length=1, choices=ACTUAL_STATUS, default='u', blank=True, help_text='Book status')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)
        ordering = ['due_back']

    def __str__(self):
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])


    def __str__(self):
        return f"{self.last_name} {self.first_name}"
