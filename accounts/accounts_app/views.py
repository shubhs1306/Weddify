import random
import string
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
# from orders.models import Order
from .rabbitmq import email_delete, email_register, email_resetpwd
from .models import Vendor
# from services.models import Service
import json
from .tasks import sendtask
from django.core import serializers

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username and password combination!')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        is_vendor = request.POST.get('is_vendor')
        service_type = request.POST.get('service_type')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    user.save()
                    messages.success(request, 'You are registerd successfully! ')

                    UserDict={"firstname":firstname, "lastname":lastname, "email":email, "username":username, "servicetitle":""}
                    email_register(json.dumps(UserDict))

                    if is_vendor:
                        vendor = Vendor.objects.create(user=user, service_type=service_type)
                        vendor.save()
                        messages.success(request, 'You are registerd as vendor successfully! ')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    vendors = Vendor.objects.filter(user=request.user.id)
    print(vendors)
    # states = Service.objects.values_list('state', flat=True).distinct()
    states = serializers.deserialize('json', sendtask('ServiceObjectList','state')) if sendtask('ServiceObjectList','state') is not None else []
    if vendors:
        is_vendor = True
        vendor = vendors[0]
        # their_services = Service.objects.order_by('-created_date').filter(vendor_id=request.user.id)
        their_services = serializers.deserialize('json', sendtask('ServiceObjectOrderBy',vendor_id=request.user.id)) if sendtask('ServiceObjectOrderBy', is_featured=True) is not None else []
        # payments = Order.objects.order_by('-created_date').filter(vendor_id=request.user.id)
        payments = serializers.deserialize('json', sendtask('OrderObjectOrderBy',vendor_id=request.user.id)) if sendtask('OrderObjectOrderBy', vendor_id=request.user.id) is not None else []
        for payment in payments:
            user = User.objects.get(id=payment.user_id)
            setattr(payment, 'user', user)
        data = {
            'payments' : payments,
            'is_vendor': is_vendor,
            'states' : states,
            'vendor' : vendor,
            'their_services' : their_services,
        }
    else:
        is_vendor = False
        vendor = None
        # payments = Order.objects.order_by('-created_date').filter(user_id=request.user.id)
        payments = serializers.deserialize('json', sendtask('OrderObjectOrderBy',user_id=request.user.id)) if sendtask('OrderObjectOrderBy', user_id=request.user.id) is not None else []
        for payment in payments:
            vendor = User.objects.get(id=payment.vendor_id)
            setattr(payment, 'vendor', vendor)
        data = {
            'payments' : payments,
            'is_vendor': is_vendor,
            'states' : states,
            'vendor' : vendor,
        }
    return render(request, 'accounts/dashboard.html', data)

def profile(request):
    vendors = Vendor.objects.filter(user=request.user.id)
    # states = Service.objects.values_list('state', flat=True).distinct()
    states = serializers.deserialize('json', sendtask('ServiceObjectList','state'))  if sendtask('ServiceObjectList','state') is not None else []
    if vendors:
        is_vendor = True
        vendor = vendors[0]
        # payments = Order.objects.order_by('-created_date').filter(vendor_id=request.user.id)
        payments = serializers.deserialize('json', sendtask('OrderObjectOrderBy',vendor_id=request.user.id)) if sendtask('OrderObjectOrderBy', vendor_id=request.user.id) is not None else []
        for payment in payments:
            user = User.objects.get(id=payment.user_id)
            setattr(payment, 'user', user)
            payment.amount = payment.amount
    else:
        is_vendor = False
        vendor = None
        # payments = Order.objects.order_by('-created_date').filter(user_id=request.user.id)
        payments = serializers.deserialize('json', sendtask('OrderObjectOrderBy',user_id=request.user.id)) if sendtask('OrderObjectOrderBy', user_id=request.user.id) is not None else []
        for payment in payments:
            vendor = User.objects.get(id=payment.vendor_id)
            setattr(payment, 'vendor', vendor)
    data = {
        'payments' : payments,
        'is_vendor': is_vendor,
        'states' : states,
        'vendor' : vendor,
    }
    return render(request, 'accounts/profile.html', data)

def update_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password != None and password != "":
                user.set_password(password)
            auth.login(request, user)
            messages.success(request, "Profile Updated Successfully")
            user.save()
            return redirect('profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('profile')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out !')
        return redirect('home')
    return redirect(request, 'home')

def delete_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            # messages.success(request, "Profile deleted successfully.")

            UserDict={"firstname":user.first_name, "lastname":user.last_name, "email":user.email, "username":user.username, "servicetitle":""}
            email_delete(json.dumps(UserDict))
            return redirect('home')
        except:
            messages.error(request, "Failed to Delete Profile")
            return redirect('profile')
        
def resetpwd(request):
    if request.method == 'POST':
        email = request.POST['email']
        emails = User.objects.values_list('email', flat=True)
        if email in emails:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            user=User.objects.get(email=email)
            user.set_password(password)
            auth.login(request, user)
            user.save()
            messages.success(request, "Password reset successfully. Check email.")

            UserDict={"firstname":user.first_name, "lastname":user.last_name, "email":user.email, "username":user.username, "servicetitle":password}
            email_resetpwd(json.dumps(UserDict))
            return redirect('login')
        else:
            messages.error(request, "Email id not found!")
            return redirect('resetpwd')
    else:
        return render(request, 'accounts/resetpwd.html')