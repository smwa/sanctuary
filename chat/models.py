from django.db import models

class Message(models.Model):
  sender = models.CharField(max_length=64)
  body = models.CharField(max_length=255)
