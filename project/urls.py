"""
URL configuration for project project.

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
from django.conf.urls.static import static
from django.conf import settings
from authentication.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library_admin/', include("library_admin.urls")),
    path('authenticate/', include("authentication.urls")),
    path('users/', include("student.urls")),
    path('books/', include("book_app.urls")),
    path('quiz/', include("quiz_app.urls")),
    path('', landing_page,name="landing_page"),
    path('', landing_page,name="landing_page"),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)