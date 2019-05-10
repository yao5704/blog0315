'''bolg0315/urls'''
from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog0315'
urlpatterns = [
    path('', views.index, name='index'),
    # 用于添加新文章的网页
    path('new_article/', views.new_article, name='new_article'),
    # 特定文章的详细页面

    path('details/<str:article_author>', views.selfblog, name='selfblog'),
    path('<int:article_id>/', views.article_detail, name='article_detail'),
    path('blogs/', views.blogs, name='blogs'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:category_id>/', views.article_category, name='article_category'),
    path('tags/<int:tag_id>/', views.article_tag, name='article_tag'),
    path('test/', views.test, name='test'),
    path('test2/<int:article_id>/', views.test2, name='test2'),
   # path('classified/<int:year>/<int:month>',views.classified,name='classified'),
   # sql3的日期检索不好用，先不弄日期归类
]
