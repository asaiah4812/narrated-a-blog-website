from django.urls import path
from . import views

app_name='article'

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'), # 文章列
    path('category/<slug:tag>/', views.article_list, name='category'), # 文章列
    path('article/<int:year>/<int:month>/<int:day>/<slug:article>/<str:pk>/', views.article_detail, name='article_detail'), # 文章列
    path('create-article', views.create_article, name='create'),
    path('commentsent/<str:pk>/', views.article_share, name='comment-sent'),
    path('<slug:article>/share/', views.article_share, name='article_share'),
    path('commentdelete/<str:pk>/', views.comment_delete, name='comment-delete'),
    path('loved/<str:pk>/', views.love_article, name='loved'),
    path('like-comment/<str:pk>/', views.like_comment, name='like'),
    path('dislike-comment/<str:pk>/', views.dislike_comment, name='dislike')
]
