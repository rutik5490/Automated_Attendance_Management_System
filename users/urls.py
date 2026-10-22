from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dean/dashboard/', views.dean_dashboard, name='dean_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]