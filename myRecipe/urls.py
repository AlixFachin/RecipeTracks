"""myRecipe URL Configuration

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
from django.urls import include, path
from django.conf.urls import i18n
from recipeViewer import views
from users import views as user_views
from django.contrib.auth import views as authentication_views

from django.conf import settings   # Needed to allow import of static files
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipeviewer/', include('recipeViewer.urls')),
    path('',views.home_view,name='recipeHome'),
    path('register/', user_views.register, name='register' ),
    path('login/',authentication_views.LoginView.as_view(template_name='users/login.html'), name='login' ),
    path('logout/',authentication_views.LogoutView.as_view(template_name='users/logout.html'), name='logout' ),
    path('profile/',user_views.profilepage, name = 'profile' ),
    path('i18n/',include('django.conf.urls.i18n')),  
    path('password/', user_views.change_password, name='change_password'),
    path('profile_picture/', user_views.change_picture, name='change_profile_picture'),
    ]


urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

