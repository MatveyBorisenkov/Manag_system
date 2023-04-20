"""manage URL Configuration

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
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.urls import path
from system.views import EntitiesListView, DocumentCreate, LoginUser, ViewFiles, FileUpdate, FileCreate, FilesToCategories, SearchFiles
from system.views import category_detail, entities_form, files_form, logout_user, UserRegister


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', EntitiesListView.as_view(), name='category-list'),
    path('category/<my_id>/', category_detail, name='category-detail'),
    path('form/', entities_form, name='entities-form'),
    path('add-document/', DocumentCreate.as_view(), name='document-form'),
    path('add-file/', FileCreate.as_view(), name='file-form'),
    path('register/', UserRegister, name='register' ),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name = 'logout'),
    path('files/', ViewFiles.as_view(), name = 'files'),
    path('file-update/', FileUpdate.as_view(), name = 'file-update'),
    path('files-cat/', FilesToCategories.as_view(), name = 'cat-files'),
    path('search-file/', SearchFiles.as_view(), name = 'search')
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    ]
