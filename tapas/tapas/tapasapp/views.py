from typing import NewType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Dish, Account

# Create your views here.

userAccount = Account.objects.get(pk=1)

def login(request):
    if(request.method == "POST"):
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        accountList = Account.objects.filter(username = uname)

        if(len(accountList) > 0):
            # returns Account object
            authenticateUser = Account.objects.get(username = uname)

            if(authenticateUser.getPassword() == pword):
                global userAccount
                userAccount = authenticateUser
                messages.success(request, 'Successfully Logged In!')
                return redirect('view_menu')
            else:
                messages.info(request, 'Invalid Login')
                return render(request, 'tapasapp/login.html')
        else:
            messages.info(request, 'Invalid Login')
            return render(request, 'tapasapp/login.html')
    else:
        return render(request, 'tapasapp/login.html')

def signup(request):
    if(request.method == "POST"):
        uname = request.POST.get('username')
        pword = request.POST.get('password')

        # returns list
        accountList = Account.objects.filter(username = uname)

        if(len(accountList) > 0):
            messages.info(request, 'Account already exists!')
            return render(request, 'tapasapp/signup.html')
        else:
            Account.objects.create(username = uname, password = pword)
            messages.info(request, 'Account created successfully!')
            return redirect('login')
    else:
        return render(request, 'tapasapp/signup.html')

def manage_account(request, pk):
    lia = get_object_or_404(Account, pk=pk)
    return render(request, 'tapasapp/manage_account.html', {'lia': lia})

def change_password(request, pk):
    loggedin_user = Account.objects.get(pk=pk)
    lia = get_object_or_404(Account, pk=pk)

    if(request.method == "POST"):
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        new_confirm = request.POST.get('confirm_new_password')

        if(loggedin_user.getPassword() == current):
            if(new == new_confirm):
                Account.objects.filter(pk=pk).update(password = new_confirm)
                messages.info(request, 'Password Successfully Changed')
                return redirect('manage_account', pk=pk)
            else:
                messages.info(request, 'New Password and Confirm New Password does not match')
                return render(request, 'tapasapp/change_password.html', {'lia':lia})
        else:
            messages.info(request, 'Supplied Wrong Current Password')
            return render(request, 'tapasapp/change_password.html', {'lia':lia})
    else:
        return render(request, 'tapasapp/change_password.html', {'lia':lia})

def delete_account(request, pk):
    Account.objects.filter(pk=pk).delete()
    return redirect('login')

def view_basic_list(request):
    dish_objects = Dish.objects.all()
    return render(request, 'tapasapp/basic_list.html', {'dishes':dish_objects})


def view_menu(request):
    dish_objects = Dish.objects.all()
    global userAccount
    return render(request, 'tapasapp/list.html', {'dishes':dish_objects, 'lia':userAccount})

def add_menu(request):
    if(request.method == "POST"):
        dishname = request.POST.get('dname')
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')

        Dish.objects.create(name = dishname, cook_time = cooktime, prep_time = preptime)

        return redirect('view_menu')
    else:
        return render(request, 'tapasapp/add_menu.html')

def success(request):
    return render(request, 'tapasapp/success.html')

def view_detail(request, pk):
    d = get_object_or_404(Dish, pk=pk)
    return render(request, 'tapasapp/view_detail.html', {'d': d})

def update_dish(request, pk):
    if(request.method == "POST"):
        cooktime = request.POST.get('ctime')
        preptime = request.POST.get('ptime')

        Dish.objects.filter(pk=pk).update(cook_time = cooktime, prep_time = preptime)

        return redirect('view_detail', pk=pk)
    else:
        d = get_object_or_404(Dish, pk=pk)
        return render(request, 'tapasapp/update_menu.html', {'d':d})

def delete_dish(request, pk):
    Dish.objects.filter(pk=pk).delete()
    return redirect('view_menu')