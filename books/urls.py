from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),               # 書籍一覧表示用（ホーム画面）
    path('add/', views.add_book, name='add_book'),  # 書籍登録画面
    path('<int:pk>/', views.book_detail, name='book_detail'),  # 書籍詳細画面
    path('<int:pk>/edit/', views.edit_book, name='edit_book'), 
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),  
]