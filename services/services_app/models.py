from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField
from services.storage_backend import PublicMediaStorage

# Create your models here.

class Service (models.Model):

    service_type_choice = (
        ('Photographer', 'Photographer'),
        ('Venue', 'Venue'),
        ('Caterer', 'Caterer'),
        ('Bridal Services', 'Bridal Services'),
    )

    state_choice = (
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Puducherry', 'Puducherry'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal')
    )

    title = models.CharField(max_length=255)
    service_type = models.CharField(choices=service_type_choice, max_length=100)
    vendor_id =models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(choices=state_choice, max_length=100)
    featured_package_price = models.IntegerField()
    service_photo_0 = models.FileField(storage=PublicMediaStorage())
    service_photo_1 = models.FileField(storage=PublicMediaStorage(), blank=True)
    service_photo_2 = models.FileField(storage=PublicMediaStorage(), blank=True)
    service_photo_3 = models.FileField(storage=PublicMediaStorage(), blank=True)
    service_photo_4 = models.FileField(storage=PublicMediaStorage(), blank=True)
    description = RichTextField()
    other_details = RichTextField()
    is_featured = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        app_label = 'services_app'

    def __str__(self):
        return self.title