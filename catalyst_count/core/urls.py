from django.urls import path,include
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('delete/<int:pk>/', views.file_delete, name='file_delete'),
    path('api/files/', views.api_file_list, name='api_file_list'),
    path('api/upload/', views.api_file_upload, name='api_file_upload'),
    path('api/delete/<int:pk>/', views.api_file_delete, name='api_file_delete'),
]