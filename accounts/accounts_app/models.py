from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Vendor (models.Model):
    service_type_choice = (
        ('Photographer', 'Photographer'),
        ('Venue', 'Venue'),
        ('Caterer', 'Caterer'),
        ('Bridal Services', 'Bridal Services'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_type = models.CharField(choices=service_type_choice,max_length=100, default=None)
    is_featured = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        app_label = 'accounts_app'
