from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_category, name='student_list'),
    path('add/', views.create_category, name='student_add'),
    path('<int:pk>/edit/', views.update_category, name='student_edit'),
    path('<int:pk>/delete/', views.delete_category, name='student_delete'),
]
