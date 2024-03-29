from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from .models import Order
from index.models import Category


# Create your views here.

@login_required
def myorder(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(buyer=user_profile, status=False, goods__name__icontains=content).reverse()
        return render(request, 'myorder.html',
                      {'user_profile': user_profile, 'orders': orders, 'message': content, 'categories': categories})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(buyer=user_profile, status=False).reverse()
        return render(request, 'myorder.html',
                      {'user_profile': user_profile, 'orders': orders, 'categories': categories})


@login_required
def completeorder(request):
    if request.method == 'POST':
        content = request.POST.get('search', '')
        user_profile = UserProfile.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(buyer=user_profile, status=True, goods__name__icontains=content).reverse()
        return render(request, 'completeorder.html',
                      {'user_profile': user_profile, 'orders': orders, 'message': content, 'categories': categories})
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        categories = Category.objects.all()
        orders = Order.objects.filter(buyer=user_profile, status=True).reverse()
        return render(request, 'completeorder.html',
                      {'user_profile': user_profile, 'orders': orders, 'categories': categories})


@login_required
def check_order(request, order_id):
    user_profile = UserProfile.objects.get(user=request.user)
    categories = Category.objects.all()
    order = Order.objects.get(id=order_id)
    order.status = True
    order.save()
    orders = Order.objects.filter(buyer=user_profile, status=True).reverse()
    return render(request, 'completeorder.html',
                  {'user_profile': user_profile, 'orders': orders, 'categories': categories})


@login_required
def delete_order(request, order_id):
    user_profile = UserProfile.objects.get(user=request.user)
    categories = Category.objects.all()
    Order.objects.filter(id=order_id).delete()
    orders = Order.objects.filter(buyer=user_profile, status=False).reverse()
    return render(request, 'myorder.html', {'user_profile': user_profile, 'orders': orders, 'categories': categories})
