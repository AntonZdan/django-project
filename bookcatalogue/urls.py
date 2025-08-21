from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import index, register, CatalogueListView, about, contacts, BookDetailView

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('catalogue/', CatalogueListView.as_view(), name='catalogue'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('book/<int:pk>', BookDetailView.as_view(template_name='book-detail.html'), name='book_detail')
]
