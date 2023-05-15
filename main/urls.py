from django.urls import path
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView



app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('about', other_page, name='about'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('acoounts/profile/change/<int:pk>/', profile_bb_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_bb_delete, name= 'profile_bb_delete'),
    path('accounts/profile/add/', profile_bb_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_bb_detail, name='profile_bb_detail'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/done/', RegisterDoneView.as_view(),  name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/асtivate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/password_reset/',
         PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.txt'), name='password_reset'),
    path('accounts/password_reset/done/',
         PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/',
         PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
]

    # path('<str:page>/', other_page, 'other'),


