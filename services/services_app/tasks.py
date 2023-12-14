from .models import Service
from services.celery import app
from django.core import serializers

@app.task(name='ServiceObjectList')
def ServiceObjectList(filter):
    return serializers.serialize('json', Service.objects.values_list(filter, flat=True).distinct())

@app.task(name='ServiceObjectGet')
def ServiceObjectGet(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Service.objects.get(**filter_args))

@app.task(name='ServiceObjectOrderBy')
def ServiceObjectOrderBy(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Service.objects.order_by('-created_date').filter(**filter_args))

def sendtask(task_name, *args, **kwargs):
    # Send the task message to the queue of the receiver app
    app.send_task(task_name, args=args, kwargs=kwargs)
