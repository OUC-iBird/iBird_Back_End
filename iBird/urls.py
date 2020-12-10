"""iBird URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from apps.utils.image_uploader import upload
from apps.utils import test

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/test_get', test.test_get),  # 仅供测试
    path('api/test_post', test.test_post),  # 仅供测试
    path('api/test_patch', test.test_patch),  # 仅供测试

    path('api/upload', upload),

    path('api/account/', include(('apps.account.urls', 'apps.account'), namespace='account')),
    path('api/prediction/', include(('apps.prediction.urls', 'apps.prediction'), namespace='prediction')),
    path('api/gallery/', include(('apps.gallery.urls', 'apps.gallery'), namespace='gallery')),
    path('api/post/', include(('apps.post.urls', 'apps.post'), namespace='post'))
]
