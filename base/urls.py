from django.urls import path
from . import views


urlpatterns = [
    path('', views.startpage, name='startpage'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('addinfo', views.addinfo, name='addinfo'),
    path('upload', views.upload, name='upload'),
    path('likepost', views.likepost, name='likepost'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('openpost/<str:pk>/', views.openpost, name='openpost'),
    path('message/<str:pk>/', views.message, name='message'),
]