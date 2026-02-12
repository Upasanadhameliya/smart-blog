from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('authors/', views.authors_list, name='authors_list'),
    path('authors/<int:pk>/follow/', views.follow_author, name='follow_author'),
    path('authors/<int:pk>/unfollow/', views.unfollow_author, name='unfollow_author'),
]
