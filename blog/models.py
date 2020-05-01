from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import timezone

class Post(models.Model):
    title = models.CharField(max_length=250)
    writer = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


# Create your models here.
