from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login, name='login'),  # login page
    path('logout/', views.logout_view, name='logout'),  # Logout page
    path('register/', views.register, name='register'),
    path('complete/<str:title>/', views.complete_todo, name='complete_todo'),  # Mark a todo item as complete
    path('delete/<int:pk>/', views.delete_todo, name='delete_todo'),  # Delete a todo item
    path('update/<int:todo_id>/', views.update_todo, name='update_todo'),  # Update a todo item
]