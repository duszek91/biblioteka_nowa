from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views import generic

from .forms import UserRegisterForm
from .models import Book, Author, BookInstance, BookGenre
from django.contrib.auth.mixins import LoginRequiredMixin


def contact(request):
    return render(request, 'contact.html', {})


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    type_genres = BookGenre.objects.all()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'type_genres': type_genres,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


def login(request):
    return render(request)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def all_books(request):
    books = Book.objects.all()
    author = Author.objects.all()
    return render(request, 'listofbooks.html', {'books': books, 'author': author})


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'  # your own name for the list as a template variable
    queryset = Book.objects.filter(title__icontains='war')[:5]  # Get 5 books containing the title war
    template_name = 'listofbooks.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

    def get_queryset(self):
        return Book.objects.all()


class AuthorListView(generic.ListView):
    model = Book
    context_object_name = 'my_author_list'  # your own name for the list as a template variable
    queryset = Author.objects.filter(first_name__icontains='war')[:5]  # Get 5 books containing the title war
    template_name = 'listofAuthors.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

    def get_queryset(self):
        return Author.objects.all()


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'book_detail.html', context={'book': book})


class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'author_detail.html', context={'author': author})


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')