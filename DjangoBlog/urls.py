"""
URL configuration for DjangoBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from DjangoBlog import settings
from blog.views import PostListView, PostDetailView, CreatePostView, AboutView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', PostListView.as_view(), name='blog/post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='blog/post_detail'),
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('about/', AboutView.as_view(), name='about_page'),
    path('logout/', LogoutView.as_view(), name='logout'),

    ### CKeditor path
    path("ckeditor", include('ckeditor_uploader.urls')),

    ### Google auth url
    path('accounts/', include('allauth.urls')),
]


urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
