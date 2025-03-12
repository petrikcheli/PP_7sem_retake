from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf.urls import handler400, handler403, handler404, handler500
from django.shortcuts import render

import traceback

def custom_400_view(request, exception):
    return render(request, "400.html", {"error_trace": exception}, status=400)

def custom_403_view(request, exception):
    return render(request, "403.html", {"error_trace": exception}, status=403)

def custom_404_view(request, exception):
    return render(request, "404.html", {"error_trace": str(exception)}, status=404)

def custom_500_view(request):
    import sys
    exc_type, exc_value, exc_traceback = sys.exc_info()  # Получаем данные об ошибке
    error_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
    return render(request, "500.html", {"error_trace": error_trace}, status=500)


handler400 = custom_400_view
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view


urlpatterns = [
    # предыдущий url входа
    # path('login/', views.user_login, name='login'),

    # url-адреса входа и выхода
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # url-адреса смены пароля
    path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    
    # url-адреса сброса пароля
    path('password-reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    # path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    #path('', views.dashboard, name='dashboard'),
    path('', views.job_list, name='job_list'),
    path('register/', views.register, name='register'),

    path('create/', views.create_job, name='create_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('search/', views.post_search, name='post_search'),
    path('my_jobs/', views.my_jobs, name='my_jobs'),

    path('my_jobs/', views.my_jobs, name='my_jobs'),
    path('job/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('job/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('employer/responses/', views.employer_responses, name='employer_responses'),
    path('responses/', views.student_responses, name='student_responses'),
    path('response/<int:response_id>/update/', views.update_response_status, name='update_response_status'),
    path('job/<int:pk>/', views.job_detail, name='job_details'),
]