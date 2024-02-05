"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myblogs import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('subscription', views.subscription, name='subscription'),
    path('blog', views.blog, name='blog'),
    path('allblogs', views.allblogs, name='allblogs'),
    path('blog_details/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('signupuser', views.signupuser, name='signupuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
    path('blog_cat/<str:blog_cat>/', views.blog_cat, name='blog_cat'),
    path('findproduct', views.findproduct, name='findproduct'),
    path('add_likes/<str:blog_id>/', views.add_likes, name='add_likes'),
    path('add_comment/<str:blog_id>/',views.add_comment, name='add_comment'),
    path('delete_comment/<int:blog_id>/<int:comment_id>/',views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:blog_id>/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)