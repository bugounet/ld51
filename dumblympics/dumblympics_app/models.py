from django.db import models

# Create your models here.
class Player(models.Model):
    uid = models.CharField(max_length=255)
    race_id = models.IntegerField()
    score = models.IntegerField(default=0)
    nick = models.CharField(max_length=255)
    
class Race(models.Model):
    open = models.BooleanField()
    start = models.DateTimeField(null=True, blank=True)
