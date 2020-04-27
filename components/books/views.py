from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .models import (
    Category,
    Book,
    ReadStatus,
    Favorite,
    Comment,
    Review
)
from ..users.decorators import admin_required
from .forms import (
    CategoryCreateForm,
    CategoryUpdateForm,
    BookCreateForm,
    BookUpdateForm
)
from ..users.models import User


class CategoryCreateView(View):
    template_name = 'category_create.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        category_create_form = CategoryCreateForm(request.user, request.POST)
        if category_create_form.is_valid():
            category_create_form.save()

            messages.success(request, 'Thêm mới danh mục thành công')

            return redirect(reverse('book:category_index'))

        return render(request, self.template_name, {'form': category_create_form})


class CategoryIndexView(View):
    template_name = 'category_index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        return render(request, self.template_name, {'categories': categories})


class CategoryUpdateView(View):
    template_name = 'category_update.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        category = get_object_or_404(Category, pk=category_id)

        return render(request, self.template_name, {'category': category})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        category = get_object_or_404(Category, pk=category_id)
        category_update_form = CategoryUpdateForm(request.POST, instance=category)
        if category_update_form.is_valid():
            category_update_form.save()

            messages.success(request, 'Cập nhật danh mục thành công')

            return redirect(reverse('book:category_index'))

        return render(request, self.template_name, {'category': category, 'form': category_update_form})


class CategoryDeleteView(View):
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        Category.objects.filter(id=category_id).delete()

        return HttpResponse('ok')


class BookCreateView(View):
    template_name = 'book_create.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()

        return render(request, self.template_name, {'categories': categories})

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_create_form = BookCreateForm(request.user, request.FILES, request.POST)
        if book_create_form.is_valid():
            book_create_form.save()

            messages.success(request, 'Thêm mới danh mục thành công')

            return redirect(reverse('book:book_index'))

        categories = Category.objects.all()

        return render(request, self.template_name, {'categories': categories, 'form': book_create_form})


class BookIndexView(View):
    template_name = 'book_index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        status = {
            0: 'chưa đọc',
            1: 'đang đọc',
            2: 'đã đọc'
        }
        icon_class = {
            0: 'fa fa-heart-o',
            1: 'fa fa-heart pinky-book-favorite-color'
        }
        status_favorite = {
            0: 'không yêu thích',
            1: 'yêu thích'
        }
        title = 'Tất cả sách'
        having = ''

        if request.GET.get('user_id'):
            user_id = int(request.GET.get('user_id'))
            username = get_object_or_404(User, pk=user_id).username
        else:
            user_id = request.user.id
            username = request.user.username
        if request.GET.get('favorite'):
            favorite = int(request.GET.get('favorite'))
            having += f"AND is_favorite={favorite} "
            title = f"Sách {status_favorite[favorite]} của {username}"
        if request.GET.get('read_status'):
            read_status = int(request.GET.get('read_status'))
            having = f"AND read_status={read_status} "
            title = f"Sách {status[read_status]} của {username}"

        book_columns = "book.id,book.name,book.description,book.image,book.publish_date,book.author,book.number_page,book.price,book.user_id,book.created_at,book.updated_at"

        sql = f"SELECT {book_columns}," \
              "IF(favorite.id, 1, 0) is_favorite," \
              "COALESCE(read_status.status, 0) AS read_status," \
              "COALESCE(AVG(review.rating), 0) AS rating, " \
              "COUNT(review.id) AS total_reviews " \
              "FROM book " \
              "LEFT JOIN favorite " \
              f"ON book.id = favorite.book_id AND favorite.user_id = {user_id} " \
              "LEFT JOIN read_status " \
              f"ON book.id = read_status.book_id AND read_status.user_id = {user_id} " \
              "LEFT JOIN review " \
              "ON book.id = review.book_id " \
              f"GROUP BY {book_columns}," \
              "favorite.id," \
              "read_status.status " \
              f"HAVING book.id IS NOT NULL {having}"

        books = Book.objects.raw(sql)

        return render(request, self.template_name, {
            'books': books,
            'status': status,
            'icon_class': icon_class,
            'title': title
        })


class BookUpdateReadStatusView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        status = int(request.POST.get('status'))

        if status:
            ReadStatus.objects.update_or_create(book_id=book_id, user_id=request.user.id, defaults={'status': status})
        else:
            ReadStatus.objects.filter(book_id=book_id, user_id=request.user.id).delete()

        return HttpResponse('ok')


class BookToggleFavoriteView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        favorite = Favorite.objects.filter(book_id=book_id, user_id=request.user.id).first()

        if favorite:
            favorite.delete()
        else:
            Favorite.objects.create(book_id=book_id, user_id=request.user.id)

        return HttpResponse('delete' if favorite else 'create')


class BookUpdateView(View):
    template_name = 'book_update.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)
        categories = Category.objects.all()

        book_categories = book.category.all()

        return render(request, self.template_name, {
            'book': book,
            'book_categories': book_categories,
            'categories': categories
        })

    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)
        book_update_form = BookUpdateForm(request.POST, request.FILES, instance=book)
        if book_update_form.is_valid():
            book_update_form.save()

            messages.success(request, 'Cập nhật danh mục thành công')

            return redirect(reverse('book:book_index'))

        categories = Category.objects.all()

        return render(request, self.template_name, {
            'book': book,
            'categories': categories,
            'form': book_update_form
        })


class BookDeleteView(View):
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)
        book.image.delete()
        book.delete()

        return HttpResponse('ok')


class BookDetailView(View):
    template_name = 'book_detail.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = get_object_or_404(Book, pk=book_id)
        comments = Comment.objects.filter(book_id=book_id).select_related('user').all()
        reviews = Review.objects.filter(book_id=book_id).select_related('user').all()

        return render(request, self.template_name, {
            'book': book,
            'comments': comments,
            'reviews': reviews
        })


class CommentCreateView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        Comment.objects.create(
            book_id=kwargs.get('id'),
            content=request.POST.get('content'),
            user=request.user
        )

        return HttpResponse('ok')


class ReviewCreateView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        Review.objects.create(
            book_id=kwargs.get('id'),
            content=request.POST.get('content'),
            rating=request.POST.get('rating'),
            user=request.user
        )

        return HttpResponse('ok')
