from django.db import models
from datetime import datetime

# Create your models here.
class Contact (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(default=datetime.now)
    message = models.TextField()

    class Meta:
        app_label = 'pages_app'