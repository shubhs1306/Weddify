import datetime
import json
from datetime import datetime
import logging
from django.utils.timezone import utc
from django.shortcuts import render, redirect
from django.contrib import messages
from .rabbitmq import email_cancelbook, email_bookvendor, email_cancelbookvendor
# from services.models import Service
from .tasks import GenerateInvoiceEmail, sendtask
from .models import Order
# from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.core import serializers

# Create your views here.

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_ACCOUNT_ID))

def payment(request):
    if request.method == 'POST':
        service_id = request.POST['service_id']
        title = request.POST['title']
        user_id = request.POST['user_id']
        vendor_id = request.POST['vendor_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        amount = serializers.deserialize('json', sendtask('ServiceObjectsGet',id=service_id)).featured_package_price
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        date_format = "%Y-%m-%d"
        duration = datetime.strptime(end_date, date_format).date()>=datetime.strptime(start_date, date_format).date()

        existing_orders=Order.objects.filter(service_id=service_id)
        
        if user_id==vendor_id:
            messages.error(request, 'Not Allowed to book own service!')
            return redirect('/services/'+service_id)
        elif (not duration):
            messages.error(request, 'Invalid Date Range!')
            return redirect('/services/'+service_id)
        elif existing_orders.exists():
                #MATCH DATES of booked service new new booking
                for ord in existing_orders:
                    if datetime.strptime(start_date, date_format).replace(tzinfo=utc)<=ord.end_date.replace(tzinfo=utc) or datetime.strptime(end_date, date_format).replace(tzinfo=utc)>=ord.start_date.replace(tzinfo=utc):
                        logger = logging.getLogger(__name__)
                        logger.info(datetime.strptime(start_date, date_format).replace(tzinfo=utc))
                        logger.info(ord.end_date.replace(tzinfo=utc))
                        logger.info(datetime.strptime(end_date, date_format).replace(tzinfo=utc))
                        logger.info(ord.start_date.replace(tzinfo=utc))
                        messages.error(request, 'This service is already booked!')
                        # return redirect('home')
                        return redirect('/services/'+service_id)
        
        order = Order(service_id=service_id, title=title, user_id=user_id, vendor_id=vendor_id, first_name=first_name,
        last_name=last_name, email=email, phone=phone, amount=amount, start_date=start_date, end_date=end_date)

        order.save()
        
        order_currency = 'INR'
        callback_url = 'http://weddify.duckdns.org/orders/handlerequest/'
        notes = {'Service Title': title, 'Name': first_name+last_name}
        razorpay_order = razorpay_client.order.create(dict(amount=amount*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
        print(razorpay_order['id'])
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        return render(request, '../templates/orders/razorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':order.amount, 'razorpay_merchant_id':settings.RAZORPAY_ID, 'callback_url':callback_url})
        
def delete_order(request, id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('/accounts/profile')
    else:
        order = Order.objects.get(id=id)
        try:
            now = datetime.utcnow().replace(tzinfo=utc)
            duration = now - order.created_date
            if duration.total_seconds() > (24*3600):
                messages.error(request, "Orders cannot be canceled after 24 hours!")
                return redirect('/accounts/dashboard')

            UserDict={"firstname":order.first_name, "lastname":order.last_name, "email":order.email, "username":"", "servicetitle":order.title}
            email_cancelbook(json.dumps(UserDict))
            Vendor=serializers.deserialize('json', sendtask('UserObjectGet',id=order.vendor_id))
            UserDict={"firstname":Vendor.first_name, "lastname":Vendor.last_name, "email":Vendor.email, "username":order.first_name, "servicetitle":order.title}
            email_cancelbookvendor(json.dumps(UserDict))

            order.delete()
            messages.success(request, "Order Canceled successfully.")
            return redirect('/accounts/dashboard')
        except:
            raise

@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            order_id = request.POST.get('razorpay_order_id','')
            signature = request.POST.get('razorpay_signature','')
            params_dict = { 
            'razorpay_order_id': order_id, 
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
            }
            try:
                order_db = Order.objects.get(razorpay_order_id=order_id)
            except:
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result==None:
                amount = order_db.amount * 100   #we have to pass in paisa
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    order_db.payment_status = 1
                    order_db.save()

                    ## For generating Invoice PDF
                    data = {
                        'order_id': order_db.order_id,
                        'transaction_id': order_db.razorpay_payment_id,
                        'email': order_db.email,
                        'phone': order_db.phone,
                        'date': str(order_db.created_date),
                        'first_name': order_db.first_name,
                        'last_name': order_db.last_name,
                        'title':order_db.title,
                        'start_date': order_db.start_date,
                        'end_date':order_db.end_date,
                        'amount': order_db.amount,
                    }
                    GenerateInvoiceEmail.delay(data)

                    #send invoice via email to customer via email (springboot)
                    Vendor=serializers.deserialize('json', sendtask('UserObjectGet',id=order_db.vendor_id))
                    Dict={"firstname":Vendor.first_name, "lastname":Vendor.last_name, "email":Vendor.email, "username":data['first_name'], "servicetitle":data['title']}
                    email_bookvendor(json.dumps(Dict))
                    messages.success(request, 'Thank you for booking. we will get back to you soon!')
                    return redirect('/services/'+order_db.service_id)
                    # return render(request, 'firstapp/payment/paymentsuccess.html',{'id':order_db.id})
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    messages.error(request, "Booking failed! In case money was deducted, it will be autorefunded in 7-10 days.")
                    return redirect('/services/'+order_db.service_id)
                    # return render(request, 'firstapp/payment/paymentfailed.html')
            else:
                order_db.payment_status = 2
                order_db.save()
                messages.error(request, "Booking failed! In case money was deducted, it will be autorefunded in 7-10 days.")
                return redirect('/services/'+order_db.service_id)
                # return render(request, 'firstapp/payment/paymentfailed.html')
        except:
            return HttpResponse("505 not found")
