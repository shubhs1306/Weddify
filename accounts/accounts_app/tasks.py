from .models import Vendor
from accounts.celery import app
from django.contrib.auth.models import User
from django.core import serializers

@app.task(name='VendorObjectList')
def VendorObjectList(filter):
    return serializers.serialize('json', Vendor.objects.values_list(filter, flat=True).distinct())

@app.task(name='VendorObjectGet')
def VendorObjectGet(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Vendor.objects.get(**filter_args))

@app.task(name='VendorObjectOrderBy')
def VendorObjectOrderBy(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Vendor.objects.order_by('-created_date').filter(**filter_args))
    
@app.task(name='UserObjectList')
def UserObjectList(filter):
    return serializers.serialize('json', User.objects.values_list(filter, flat=True).distinct())

@app.task(name='UserObjectGet')
def UserObjectGet(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', User.objects.get(**filter_args))

@app.task(name='UserObjectGet')
def UserObjectOrderBy(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', User.objects.order_by('-created_date').filter(**filter_args))

def sendtask(task_name, *args, **kwargs):
    # Send the task message to the queue of the receiver app
    app.send_task(task_name, args=args, kwargs=kwargs)
