"""ppsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls import handler400, handler403, handler404, handler500
from django.shortcuts import render
import traceback
from django.conf import settings
from django.conf.urls.static import static

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
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('account/', include('account.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
