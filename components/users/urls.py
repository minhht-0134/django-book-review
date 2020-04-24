from django.urls import path

from .views import (
    UserLoginView,
    UserRegisterView,
    UserLogoutView,
    UserTimelineView,
    UserMyProfileView,
    MemberIndexView,
    MemberToggleFollowView,
    RequestCreateView,
    MyRequestView,
    RequestUpdateView,
    RequestDeleteView,
    RequestIndexView,
    RequestChangeStatusView
)

app_name = 'user'

urlpatterns = [
    path('login', UserLoginView.as_view(), name='login'),
    path('register', UserRegisterView.as_view(), name='register'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('', UserTimelineView.as_view(), name='timeline'),
    path('my-profile', UserMyProfileView.as_view(), name='my_profile'),
    path('member', MemberIndexView.as_view(), name='member_index'),
    path('member/<int:following_id>/toggle-follow', MemberToggleFollowView.as_view(), name='member_toggle_follow'),
    path('request/create', RequestCreateView.as_view(), name='request_create'),
    path('request/my-request', MyRequestView.as_view(), name='my_request'),
    path('request/<int:id>/edit', RequestUpdateView.as_view(), name='request_update'),
    path('request/<int:id>/del', RequestDeleteView.as_view(), name='request_delete'),
    path('request/', RequestIndexView.as_view(), name='request_index'),
    path('request/<int:id>/change-status', RequestChangeStatusView.as_view(), name='request_change_status'),
]
