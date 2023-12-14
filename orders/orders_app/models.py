from django.db import models
from datetime import datetime

from orders.storage_backend import PrivateMediaStorage

# Create your models here.
class Order(models.Model):
    payment_status_choices = (
        (1, 'SUCCESS'),
        (2, 'FAILURE' ),
        (3, 'PENDING'),
    )
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=50, blank=True)
    service_id = models.IntegerField(default=1)
    vendor_id = models.IntegerField(default=1)
    user_id = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    payment_status = models.IntegerField(choices = payment_status_choices, default=3)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
    # related to razorpay
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    receiptpdf = models.FileField(storage=PrivateMediaStorage())

    def save(self, *args, **kwargs):
        if (self.order_id is None and self.created_date and self.id):
            self.order_id=self.created_date.strftime('OD%Y%m%d%H%M%S%fID')+str(self.id)
        return super().save(*args, **kwargs)

    class Meta:
        app_label = 'orders_app'

    def __str__(self):
        return self.first_name