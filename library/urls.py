from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Books
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # Members
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.member_add, name='member_add'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),

    # Issue / Return
    path('issue/', views.issue_book, name='issue_book'),
    path('issued/', views.issued_books, name='issued_books'),
    path('issued/<int:pk>/return/', views.return_book, name='return_book'),
    path('returned/', views.returned_books, name='returned_books'),
    path('overdue/', views.overdue_books, name='overdue_books'),
]





