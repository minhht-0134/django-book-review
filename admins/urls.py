from django.urls import path, include
from admins.components.dashboard import *
from admins.components.bookmanager import *
from admins.components.requestmanager import *
from admins.components.commentmanager import *
from admins.components.categorymanager import *
from admins.components.quotemanager import *
from admins.components.ratemanager import *
from admins.components.usermanager import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    path('book-manager/', BookManagerView.as_view(), name='book-manager'),
    path('book-manager/create-book', CreateBookView.as_view(), name='create-book'),
    path('book-manager/book/<int:pk>/delete', EditOrDeleteBookView.as_view(), name='delete-book'),
    path('book-manager/book/<int:pk>/edit', EditOrDeleteBookView.as_view(), name='edit-book'),
    
    path('request-manager/', RequestManagerView.as_view(), name='request-manager'),
    path('request-manager/request/<int:request_id>/approve', ApproveRequestView.as_view(), name='approve-request'),
    path('request-manager/request/<int:request_id>/cancel', CancelRequestView.as_view(), name='cancel-request'),
    path('request-manager/request/<int:request_id>/delete', DeleteRequestView.as_view(), name='delete-request'),
    
    path('comment-manager/', CommentManagerView.as_view(), name='comment-manager'),
    path('request-manager/comment/<int:comment_id>/delete', DeleteCommentView.as_view(), name='delete-comment'),
    
    path('rate-manager/', RateManagerView.as_view(), name='rate-manager'),
    path('rate-manager/rate/<int:rate_id>/delete', DeleteRateView.as_view(), name='delete-rate'),
    
    path('category-manager/', CategoryManagerView.as_view(), name='category-manager'),
    path('category-manager/create-category', CreateCategoryView.as_view(), name='create-category'),
    path('category-manager/category/<int:category_id>/edit', EditOrDeleteCategoryView.as_view(), name='edit-category'),
    path('category-manager/category/<int:category_id>/delete', EditOrDeleteCategoryView.as_view(), name='delete-category'),
    
    path('quote-manager/', QuoteManagerView.as_view(), name='quote-manager'),
    path('quote-manager/create-quote', CreateQuoteView.as_view(), name='create-quote'),
    path('quote-manager/quote/<int:quote_id>/edit', EditOrDeleteQuoteView.as_view(), name='edit-quote'),
    path('quote-manager/quote/<int:quote_id>/delete', EditOrDeleteQuoteView.as_view(), name='delete-quote'),
    
    path('user-manager/', UserManagerView.as_view(), name='user-manager'),
    path('user-manager/user/<int:user_id>/delete', ChangeOrDeleteUserView.as_view(), name='delete-user'),
    path('user-manager/user/<int:user_id>/change-password', ChangeOrDeleteUserView.as_view(), name='changepw-user'),
]