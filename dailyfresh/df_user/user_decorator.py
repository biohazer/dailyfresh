#coding=utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

#如果未登录则跳转到登录页面

def login(func):
	def login_fun(request,*args,**kwargs):#
		if request.session.has_key('user_id'):
			return func(request,*args,**kwargs)
			#在我们登录成功之后，写的有一个request.session信息
			#因为有些function有除了request之外的其他写进URL参数，
			#所以接收的参数和return的参数都要做到兼容参数

		else:
			red=HttpResponseRedirect('/user/login/')
			red.set_cookie('url',request.get_full_path())
			return red
			#当用户登录完了之后，要跳转回登录页之前的页面。在这里存一个当前页面全地址的cookie
			#request.path()是不带参数的部分地址，用来匹配URL可以。
			#request.get_full_path()是带参数的全部地址，用来精准返回
			#在判断login之后的代码里有跳转到cookie页
			#url=request.COOKIES.get('url','/')
			#red=HttpResponseRedirect(url)
			

	return login_fun
