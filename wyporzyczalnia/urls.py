from django.urls import path
from . import views
from .views import all_books

urlpatterns = [
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed')
    # path('wszystkie/', wszystkie_filmy, name='wszystkie_filmy'),
    # path('nowy/', nowy_film, name='nowy_film'),
    # path('edytuj/<int:id>', edytuj_film, name='edytuj_film'),
    # path('usun/<int:id>', usun_film, name='usun_film')
]