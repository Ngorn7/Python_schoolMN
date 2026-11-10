from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_subject, name='subject_list'),
    path('add/', views.create_subject, name='subject_add'),
    path('<int:pk>/edit/', views.update_subject, name='subject_edit'),
    path('<int:pk>/delete/', views.delete_subject, name='subject_delete'),
]
