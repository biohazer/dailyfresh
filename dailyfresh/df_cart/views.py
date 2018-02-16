#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from df_user import user_decorator
from models import *

# Create your views here.


@user_decorator.login
def cart(request):
	uid=request.session['user_id']
	carts=CartInfo.objects.filter(user_id=uid)
	#得到当前用户的所有购物车信息
	context={'title':'购物车',
			'page_name':1,
			'carts':carts,
			}
	return render(request,'df_cart/cart.html',context)


@user_decorator.login
def add(request,gid,count):
	#用户uid购买了gid商品，数量为count
	uid=request.session['user_id']
	gid=int(gid)
	count=int(count)
	#查看购物车里是否有此商品，如果有就添加，如果没哟就新增
	carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
	if len(carts)>=1:
		cart=carts[0]
		cart.count=cart.count+count
		#本身商品的数量+传参过来的商品数量
	else:
		cart=CartInfo()
		cart.user_id=uid
		cart.goods_id=gid
		cart.count=count

	cart.save()

	if request.is_ajax():
		count=CartInfo.objects.filter(user_id=request.session['user_id']).count()
		return JsonResponse({'count':count})
		#判断是否是ajax的请求，如果是就返回一个json格式的数据到界面的加入购物车选项

	else:
		return redirect('/cart/')

@user_decorator.login
def edit(request,cart_id,count):
	try:
		cart=CartInfo.objects.get(pk=int(cart_id))#get(pk=)和get(id=)可以互换
		count1=cart.count=int(count)
		cart.save()
		data={'ok':0}#如果正常返回0，如果不正常返回count的值
	except Exception as e:
		data={'ok':count1}
		return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
	try:
		cart=CartInfo.objects.get(pk=int(cart_id))
		cart.delete()
		data={'ok':1}
	except Exception as e:
		data={'ok':0}
	return JsonResponse(data)
