from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from django.contrib import messages

# 書籍一覧（ホーム画面）※ログイン必須
@login_required(login_url='login')
def home(request):
    status_filter = request.GET.get('status', 'all')  # ステータスフィルター
    author_query = request.GET.get('q', '')           # 著者名検索クエリ（空文字で初期化）
    rating_filter = request.GET.get('rating', '')       # おすすめ度フィルター


    # ユーザーの書籍をベースに
    books = Book.objects.filter(user=request.user)

    # ステータスフィルター
    if status_filter == 'reading':
        books = books.filter(status='reading')
    elif status_filter == 'interested':
        books = books.filter(status='interested')
    elif status_filter == 'finished':
        books = books.filter(status='finished')

    # 著者名検索（部分一致）
    if author_query:
        books = books.filter(author__icontains=author_query)

    # おすすめ度フィルター
    if rating_filter.isdigit():  # 1〜5 の数値が入力されている場合
        books = books.filter(rating=int(rating_filter))
    
    return render(request, 'books/home.html', {
        'books': books,
        'status_filter': status_filter,
        'author_query': author_query,
        'rating_filter': rating_filter,
    })
    
# 書籍登録画面
@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # ログインユーザーを紐付け
            book.save()
            return redirect('home')  # 登録後はホームへ
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

# 書籍詳細画面
@login_required(login_url='login')
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)  # 他人の本は見られないよう制限
    return render(request, 'books/detail.html', {'book': book})

# 書籍編集画面
@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, '書籍情報を更新しました。')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)

    if request.method == 'POST':
        book.delete()
        messages.success(request, '書籍を削除しました。')
        return redirect('home')

    return render(request, 'books/delete_confirm.html', {'book': book})
