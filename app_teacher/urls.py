from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_teacher, name='teacher_list'),
    path('add/', views.create_teacher, name='teacher_add'),
    path('<int:pk>/edit/', views.update_teacher, name='teacher_edit'),
    path('<int:pk>/delete/', views.delete_teacher, name='teacher_delete'),
]
