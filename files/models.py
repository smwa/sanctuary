from django.db import models
import os

def uploadTo(root):
  def wrapper(instance, filename):
    filename = instance.md5
    return os.path.join(root, filename)
  return wrapper

class Hash(models.Model):
    md5 = models.CharField(max_length=40)
    size = models.IntegerField()
    content = models.FileField(upload_to=uploadTo('files/'))

class File(models.Model):
    label = models.CharField(max_length=64)
    hash = models.ForeignKey(Hash, on_delete=models.CASCADE)
