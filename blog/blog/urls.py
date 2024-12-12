"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import RegisterView, LoginView, ActivateAccountView, CreateSuperUserView, refresh_token, get_username

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog_app.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<str:email_token>/', ActivateAccountView.as_view(), name='activate_account'),
    path('create-superuser/', CreateSuperUserView.as_view(), name='create_superuser'),
    path('refresh_token/<token>/', refresh_token, name='refresh_token'),
    path('get_username/<author_id>', get_username , name='get_username'),
]
