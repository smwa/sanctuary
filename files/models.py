from django.db import models

class Hash(models.Model):
    md5 = models.CharField(max_length=40)
    content = models.FileField(upload_to='uploads/')

class File(models.Model):
    label = models.CharField(max_length=64)
    size = models.IntegerField()
    hash = models.ForeignKey(Hash, on_delete=models.CASCADE)
