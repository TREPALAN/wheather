from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class Wheather(models.Model):
    city = models.CharField(unique=True, max_length=100)
    feels_like = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    visibility = models.FloatField()
    wind_speed = models.FloatField()
    icon = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  

    def serialize(self):
        return {
            "id": self.pk,
            "city": self.city,
            "feels_like": self.feels_like,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "temperature": self.temperature,
            "visibility": self.visibility,
            "wind_speed": self.wind_speed,
            "icon": self.icon,
            "created_at": self.created_at.strftime('%B %d, %I:%M:%S %p')
        }
