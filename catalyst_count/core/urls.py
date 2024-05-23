from django.urls import path,include
from . import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('query-builder', views.query_builder, name='query_builder'),
    # path('delete/<int:pk>/', views.file_delete, name='file_delete'),
    path('all_users',views.all_users,name="all_users"),
    # path('api/files/', views.api_file_list, name='api_file_list'),
    path('api/upload/', views.api_file_upload, name='api_file_upload'),
    path('api/query-builder/', views.api_query_builder, name='api_query_builder'),
    # path('api/delete/<int:pk>/', views.api_file_delete, name='api_file_delete'),
     path('api/register/', views.api_register, name='api_register'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    

]