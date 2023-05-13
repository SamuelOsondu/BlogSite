from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    # path('', views.BlogListView.as_view(), name='blog'),
    path('post/<int:post_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post, name='post'),
    path('<int:post_id>/send_email/', views.send_email, name='send_email'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
