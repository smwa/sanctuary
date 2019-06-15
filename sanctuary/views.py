from django.http import HttpResponse
from django.conf import settings
import os

def index(request):
  indexFilename = os.path.join(settings.STATICFILES_DIRS[0], "..", "index.html")
  indexHandle = open(indexFilename)
  response = HttpResponse(content=indexHandle, content_type="text/html")
  return response
