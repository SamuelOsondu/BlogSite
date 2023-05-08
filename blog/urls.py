from django.urls import path
from blog import views


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('post/<int:post_id>/', views.post, name='post'),
]
