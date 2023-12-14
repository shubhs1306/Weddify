from django.shortcuts import render, get_object_or_404, redirect
from .models import Service
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.
def services(request):
    services = Service.objects.order_by('-created_date')
    paginator = Paginator(services, 4)
    page = request.GET.get('page')
    paged_vanues = paginator.get_page(page)
    city_search = Service.objects.values_list('city', flat=True).distinct()
    state_search = Service.objects.values_list('state', flat=True).distinct()
    service_search = Service.objects.values_list('service_type', flat=True).distinct()
    data = {
        'services' : paged_vanues,
        'city_search' : city_search,
        'state_search' : state_search,
        'service_search' : service_search,
    }
    return render(request, 'services/services.html', data)

def service_detail(request, id):
    services = Service.objects.all()
    single_service = get_object_or_404(Service, pk=id)
    data = {
        'single_service' : single_service,
        'services' : services,
    }
    return render(request, 'pages/service_detail.html', data)

def add_service(request, id):
    if request.method == 'POST':
        title = request.POST['title']
        service_type = request.POST['service_type']
        # vendor_id = request.POST['vendor_id']
        vendor_id = id
        city = request.POST['city']
        state = request.POST['state']
        featured_package_price = request.POST['featured_package_price']
        service_photo_0 = request.FILES['service_photo_0']
        service_photo_1 = request.FILES['service_photo_1']
        service_photo_2 = request.FILES['service_photo_2']
        service_photo_3 = request.FILES['service_photo_3']
        service_photo_4 = request.FILES['service_photo_4']
        description = request.POST['description']
        other_details = request.POST['other_details']

        service = Service(title=title, service_type=service_type, vendor_id=vendor_id, city=city, state=state, featured_package_price=featured_package_price,
        service_photo_0=service_photo_0, service_photo_1=service_photo_1, service_photo_2=service_photo_2, service_photo_3=service_photo_3, 
        service_photo_4=service_photo_4, description=description, other_details=other_details)
        service.save()
        messages.success(request, 'Added successfully !')
        return redirect('dashboard')
    return render(request, 'services/addservice.html')

def update_service(request, id):
    if request.method == "POST":
        title = request.POST['title']
        service_type = request.POST['service_type']
        vendor_id = request.POST['vendor_id']
        city = request.POST['city']
        state = request.POST['state']
        featured_package_price = request.POST['featured_package_price']
        service_photo_0 = request.FILES['service_photo_0']
        service_photo_1 = request.FILES['service_photo_1']
        service_photo_2 = request.FILES['service_photo_2']
        service_photo_3 = request.FILES['service_photo_3']
        service_photo_4 = request.FILES['service_photo_4']
        description = request.POST['description']
        other_details = request.POST['other_details']
        # service_id = request.POST['service_id']
        service_id = id
        try:
            service = Service.objects.get(id=service_id)
            service.title = title
            service.service_type = service_type
            service.vendor_id = vendor_id
            service.city = city
            service.state = state
            service.featured_package_price = featured_package_price
            service.service_photo_0 = service_photo_0
            service.service_photo_1 = service_photo_1
            service.service_photo_2 = service_photo_2
            service.service_photo_3 = service_photo_3
            service.service_photo_4 = service_photo_4
            service.description = description
            service.other_details = other_details
            service.save()
            messages.success(request, "Service Updated Successfully")
            return redirect('dashboard')
        except:
            messages.error(request, "Failed to update Service")
            return render(request, 'services/updateservice.html')
    return render(request, 'services/updateservice.html')
             

def delete_service(request, id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('dashboard')
    else:
        try:
            service = Service.objects.get(id=id)
            service.delete()
            messages.success(request, "Service deleted successfully.")
            return redirect('dashboard')
        except:
            messages.error(request, "Failed to Delete Service")
            return redirect('dashboard')