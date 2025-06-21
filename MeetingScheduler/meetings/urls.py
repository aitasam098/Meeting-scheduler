from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='home'), 
    path('Signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book-meeting/', views.book_meeting, name='book_meeting'),
    path('meeting-status/', views.meeting_status, name='meeting_status'),
    
]