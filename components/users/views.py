from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from .forms import (
    RegisterForm,
    LoginForm,
    PasswordChangeForm,
    RequestCreateForm,
    RequestUpdateForm
)
from .models import (
    User,
    Request,
    Follow
)
from .decorators import admin_required


class UserRegisterView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        logout(request)

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            login(request, user)

            return redirect(reverse('user:timeline'))

        return render(request, self.template_name, {'form': register_form})


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('user:login'))


class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        logout(request)

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
            login(request, user)

            return redirect(reverse('user:timeline'))

        return render(request, self.template_name, {'form': login_form})


class UserTimelineView(View):
    template_name = 'timeline.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserMyProfileView(View):
    template_name = 'my_profile.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if password_change_form.is_valid():
            user = password_change_form.save()
            login(request, user)

            messages.success(request, 'Thay đổi mật khẩu thành công')

            return redirect(reverse('user:my_profile'))

        return render(request, self.template_name, {'form': password_change_form})


class MemberIndexView(View):
    template_name = 'member_index.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        status_title = {
            0: 'không theo dõi',
            1: 'đang theo dõi'
        }
        roles = {
            1: 'Quản trị viên',
            2: 'Thành viên'
        }
        status = {
            0: 'Theo dõi',
            1: 'Đang theo dõi'
        }
        icon_class = {
            0: 'fa fa-rss',
            1: 'fa fa-check'
        }
        title = 'Tất cả thành viên'
        having = ''

        if request.GET.get('user_id'):
            user_id = int(request.GET.get('user_id'))
            username = get_object_or_404(User, pk=user_id).username
        else:
            user_id = request.user.id
            username = request.user.username
        if request.GET.get('following'):
            following = int(request.GET.get('following'))
            having += f"AND is_following={following} "
            title = f"Danh sách thành viên {username} {status_title[following]}"
        if request.GET.get('follower'):
            follower = int(request.GET.get('follower'))
            having = f"AND is_follower={follower} "
            title = f"Danh sách thành viên {status_title[follower]} {username}"

        user_column = "user.id,user.password,user.username,user.email,user.role"

        sql = f"SELECT {user_column}," \
              "IF(following.id, 1, 0) is_following," \
              "IF(follower.id, 1, 0) is_follower " \
              "FROM user " \
              "LEFT JOIN follow AS following " \
              f"ON user.id = following.following_id AND following.follower_id = {user_id} " \
              "LEFT JOIN follow AS follower " \
              f"ON user.id = follower.follower_id AND follower.following_id = {user_id} " \
              f"GROUP BY {user_column}," \
              "following.id," \
              "follower.id " \
              f"HAVING user.id IS NOT NULL {having} " \
              "ORDER BY user.role"

        members = User.objects.raw(sql)

        return render(request, self.template_name, {
            'members': members,
            'roles': roles,
            'title': title,
            'status': status,
            'icon_class': icon_class
        })


class MemberToggleFollowView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        following_id = kwargs.get('following_id')
        follow = Follow.objects.filter(follower=request.user, following_id=following_id).first()

        if follow:
            follow.delete()
        else:
            Follow.objects.create(follower=request.user, following_id=following_id)

        return HttpResponse('delete' if follow else 'create')


class RequestCreateView(View):
    template_name = 'request_create.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_create_form = RequestCreateForm(request.user, request.POST)
        if request_create_form.is_valid():
            request_create_form.save()

            messages.success(request, 'Thêm mới yêu cầu thành công')

            return redirect(reverse('user:my_request'))

        return render(request, self.template_name, {'form': request_create_form})


class MyRequestView(View):
    template_name = 'my_request.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        status = {
            1: 'Chờ duyệt',
            2: 'Phê duyệt',
            3: 'Hoàn thành'
        }

        my_request = Request.objects.filter(user=request.user).all()

        return render(request, self.template_name, {'my_request': my_request, 'status': status})


class RequestUpdateView(View):
    template_name = 'request_update.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        request_object = get_object_or_404(Request, pk=request_id)

        if request_object.status != 1:
            messages.error(request, 'Yêu cầu đã được phê duyệt bạn không thể chỉnh sửa')
            return redirect(reverse('user:my_request'))

        return render(request, self.template_name, {'request_object': request_object})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        request_object = get_object_or_404(Request, pk=request_id)
        request_update_form = RequestUpdateForm(request.POST, instance=request_object)

        if request_update_form.is_valid():
            if request_object.status != 1:
                messages.error(request, 'Yêu cầu đã được phê duyệt bạn không thể chỉnh sửa')
            else:
                request_update_form.save()
                messages.success(request, 'Cập nhật yêu cầu thành công')

            return redirect(reverse('user:my_request'))

        return render(request, self.template_name, {'request_object': request_object, 'form': request_update_form})


class RequestDeleteView(View):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        request_object = get_object_or_404(Request, pk=request_id)

        if (request.user.role == 2) and (request_object.status != 1):
            return HttpResponseForbidden('Yêu cầu đã được phê duyệt bạn không thể xoá')

        if (request.user.role == 1) and (request_object.status == 3):
            return HttpResponseForbidden('Yêu cầu đã được hoàn thành bạn không thể xoá')

        request_object.delete()

        return HttpResponse('ok')


class RequestIndexView(View):
    template_name = 'request_index.html'

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        status = {
            1: 'Chờ duyệt',
            2: 'Phê duyệt',
            3: 'Hoàn thành'
        }

        requests = Request.objects.prefetch_related('user').order_by('-id').all()

        return render(request, self.template_name, {'requests': requests, 'status': status})


class RequestChangeStatusView(View):
    @method_decorator(admin_required)
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        status = int(request.POST.get('status'))

        request_object = get_object_or_404(Request, pk=request_id)

        if request_object.status == 3:
            return HttpResponseForbidden('Yêu cầu đã được hoàn thành bạn không thể cập nhật')

        request_object.status = status
        request_object.save()

        return HttpResponse('ok')
