#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from django.db import transaction#在django里面要使用事务，要把这个引过来
from models import *
from datetime import datetime
from decimal import Decimal


# Create your views here.
#建立order页面的信息view
@user_decorator.login
def order(request):
    #查询用户对象
    user=UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息,找到当前user的所有cart的ID
    get=request.GET
    cart_ids=get.getlist('cart_id')#得到了全部的cart商品ID
    cart_ids1=[int(item) for item in cart_ids]
    carts=CartInfo.objects.filter(id__in=cart_ids1)
    #构造传递到模版中的数据
    context={'title':'提交订单',
             'page_name':1,
             'carts':carts,
             'user':user,
             'cart_ids':','.join(cart_ids)}
    return render(request,'df_order/order.html',context)

#事务：一旦操作失败则全部回退
#1，创建订单对象
#2，判断商品的库存
#3，创建订单对象
#4，修改商品库存
#5，删除购物车

@transaction.atomic()#使用事务要加这个
@user_decorator.login()
def order_handle(request):
    tran_id=transaction.savepoint()#保存一个点，将来可以回到这个点来
    #接受购物车编号
    cart_ids=request.POST.get('cart_ids')#5,6
    try:
        #创建订单对象
        order=OrderInfo()
        now=datetime.now()
        uid=request.session['user_id']
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        #print order.oid
        order.odate=now
        order.ototal=Decimal(request.POST.get('total'))
        order.save()
        #创建详单对。遍历创建购物车信息
        cart_ids1=[int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail=OrderDetailInfo()
            detail.order=order
            #查询购物车信息
            cart=CartInfo.objects.get(id=id1)
            #判断商品库存
            goods=cart.goods
            if goods.gkucun>=cart.count: #如果库存大于购买数量
                #减少商品库存
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()
                #完善购物车数据
                detail.goods_id=goods.id
                detail.price=goods.gprice
                detail.save()
                #删除购物车数据
                cart.delete()
            else:#如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)#如果上面某时刻库存数量不够了，
                # 回退到开始创建的那个点，上面所有对数据库的更改都失，回退到购物车页面让用户修改库存
                return redirect('/cart/')
            #return HttpResponse('no')
        transaction.saveoint_commit(tran_id)#上面都成果了，保存点提交
    except Exception as e:
        print '========================%s'%e
        transaction.savepoint_rollback(tran_id)#如果在进行事务过程中出现任何的异常，进行事务的回退

    # return Httpresponse('ok')
    #转到用户中心的我的订单页
    #在用户中心-我的订单 查询所有的订单信息，并且呈现出来就可以了

    return redirect('/user/order/')






@user_decorator.login
def pay(request,oid):
    order=OrderInfo.objects.get(oid=oid)
    order.oIsPay=True
    order.save()
    context={'order':order}
    return render(request,'df_order/pay.html',context)


