import json
from orders_app.rabbitmq import email_book
from .models import Order
from orders.celery import app
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.core.files import File
from django.core import serializers

@app.task(name='OrderObjectList')
def OrderObjectList(filter):
    return serializers.serialize('json', Order.objects.values_list(filter, flat=True).distinct())

@app.task(name='OrderObjectGet')
def OrderObjectGet(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Order.objects.get(**filter_args))

@app.task(name='OrderObjectOrderBy')
def OrderObjectOrderBy(**kwargs):
    if kwargs:
        key, value = next(iter(kwargs.items()))
        filter_args = {key: value}
        return serializers.serialize('json', Order.objects.order_by('-created_date').filter(**filter_args))
    
@app.task(name='GenerateInvoiceEmail')
def GenerateInvoiceEmail(data):
    # data = {
        # 'order_id': order_db.order_id,
        # 'transaction_id': order_db.razorpay_payment_id,
        # 'email': order_db.email,
        # 'phone': order_db.phone,
        # 'date': str(order_db.created_date),
        # 'first_name': order_db.first_name,
        # 'last_name': order_db.last_name,
        # 'title':order_db.title,
        # 'start_date': order_db.start_date,
        # 'end_date':order_db.end_date,
        # 'amount': order_db.amount,
    # }
    template = get_template('orders/invoice.html')
    html  = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    filename = 'Invoice_' + data['order_id'] + '.pdf'
    order=Order.objects.get(order_id=data['order_id'])
    pdf_file = File(pdf, name=filename)
    pdf_file.content_type = 'application/pdf'
    order.receiptpdf = pdf
    order.save()
    recipt_url = order.receiptpdf.url
    Dict={"firstname":data['first_name'], "lastname":data['order_id'], "email":data['email'], "username":recipt_url, "servicetitle":data['title']}
    email_book(json.dumps(Dict))

def sendtask(task_name, *args, **kwargs):
    # Send the task message to the queue of the receiver app
    app.send_task(task_name, args=args, kwargs=kwargs)
