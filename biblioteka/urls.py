from django.contrib import admin
from django.urls import path, include


from wyporzyczalnia import views as w_views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings

from wyporzyczalnia.views import all_books

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', w_views.index, name='index'),
    path('contact/', w_views.contact, name='contact'),
    path('wyporzyczalnia/', include('wyporzyczalnia.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', w_views.register, name='register'),
    path('booklist/', w_views.BookListView.as_view(), name="all_books"),
    path('accounts/', include('django.contrib.auth.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
