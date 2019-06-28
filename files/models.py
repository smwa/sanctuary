from django.db import models
import os

def uploadTo(instance, filename):
  return os.path.join("files", instance.md5)

class Hash(models.Model):
    md5 = models.CharField(max_length=40)
    size = models.IntegerField()
    content = models.FileField(upload_to=uploadTo)

class File(models.Model):
    label = models.CharField(max_length=64)
    hash = models.ForeignKey(Hash, on_delete=models.CASCADE)
