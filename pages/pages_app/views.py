import json
from django.shortcuts import render
from pages_app.models import Contact
from pages_app.rabbitmq import email_contactus
from pages_app.tasks import sendtask
from django.contrib import messages
from django.core import serializers
# Create your views here.

def handler404(request, exception=None):
    return render(request, 'includes/404.html')

def home(request):
    # featured_services = serializers.deserialize('json', sendtask('ServiceObjectOrderBy', is_featured=True)) if sendtask('ServiceObjectOrderBy', is_featured=True) is not None else []
    all_services = serializers.deserialize('json', sendtask('ServiceObjectOrderBy', is_featured=True)) if sendtask('ServiceObjectOrderBy', is_featured=True) is not None else []
    city_search = serializers.deserialize('json', sendtask('ServiceObjectList','city'))  if sendtask('ServiceObjectList','city') is not None else []
    state_search = serializers.deserialize('json', sendtask('ServiceObjectList','state'))  if sendtask('ServiceObjectList','state') is not None else []
    service_search = serializers.deserialize('json', sendtask('VendorObjectList','service_type'))  if sendtask('VendorObjectList','service_type') is not None else []
    data = {
        'featured_services' : all_services,
        'city_search' : city_search,
        'state_search' : state_search,
        'service_search' : service_search,
        'all_services' : all_services,
    }
    return render(request, 'pages/home.html', data)

def search(request):
    services = serializers.deserialize('json', sendtask('ServiceObjectOrderBy', is_featured=True)) if sendtask('ServiceObjectOrderBy', is_featured=True) is not None else []
    city_search = serializers.deserialize('json', sendtask('ServiceObjectList','city'))  if sendtask('ServiceObjectList','city') is not None else []
    state_search = serializers.deserialize('json', sendtask('ServiceObjectList','state'))  if sendtask('ServiceObjectList','state') is not None else []
    service_search = serializers.serialize('json', sendtask('ServiceObjectList','service_type'))  if sendtask('ServiceObjectList','service_type') is not None else []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            services = services.filter(description__icontains=keyword) if services!=[] else []

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            services = services.filter(city__iexact=city) if services!=[] else []

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            services = services.filter(state__iexact=state) if services!=[] else []
    
    if 'service_type' in request.GET:
        service_type = request.GET['service_type']
        if service_type:
            services = services.filter(service_type__iexact=service_type) if services!=[] else []

    if 'min_featured_package_price' in request.GET:
        min_featured_package_price = request.GET['min_featured_package_price']
        max_featured_package_price = request.GET['max_featured_package_price']
        if max_featured_package_price:
           services = services.filter(featured_package_price__gte=min_featured_package_price, featured_package_price__lte=max_featured_package_price) if services!=[] else []
    data = {
        'services' : services,
        'city_search' : city_search,
        'state_search' : state_search,
        'service_search' : service_search,
    }
    return render(request, 'pages/search.html', data)

def contactus (request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        message = request.POST['message']
        if message != None or message != '':
            contact = Contact(first_name=firstname, last_name=lastname, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')

            Dict={"firstname":firstname, "lastname":lastname, "email":email, "username":phone, "servicetitle":message}
            email_contactus(json.dumps(Dict))
            return render(request, 'pages/contact-us.html')
        else:
            messages.error(request, 'Cannot send empty message!')
            return render(request, 'pages/contact-us.html')
    else:
        return render(request, 'pages/contact-us.html')
