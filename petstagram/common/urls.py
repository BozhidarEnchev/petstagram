from django.urls import path
from petstagram.common import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('like/<int:pk>/', views.like_functionality, name='like'),
    path('share/<int:pk>/', views.copy_link_to_clipboard, name='share'),
]
