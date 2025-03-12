from django.urls import path
from . import views

app_name = 'blog'

from django.conf.urls import handler400, handler403, handler404, handler500
from django.shortcuts import render
import traceback

def custom_400_view(request, exception):
    return render(request, "400.html", status=400)

def custom_403_view(request, exception):
    return render(request, "403.html", status=403)

def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

def custom_500_view(request):
    error_trace = traceback.format_exc()  # Получаем текст ошибки
    return render(request, "500.html", {"error_trace": error_trace}, status=500)

handler400 = custom_400_view
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view


urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    #path('search/', views.post_search, name='post_search'),
]