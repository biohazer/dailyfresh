from django.conf.urls import include, url
from . import views
from views import *#为了自定义上下文

urlpatterns=[
	url('^$',views.index),
	url('^list(\d+)_(\d+)_(\d+)/$',views.list),
	url('^(\d+)/$',views.details),
	url(r'search/',MySearchView()), #为了购物车里显示添加了几个记，为了search-template页面可以引用上下文
]