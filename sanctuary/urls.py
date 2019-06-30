"""sanctuary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from sanctuary.views import index

captivePortalUrl = "http://{}/static/captive_portal.html".format(settings.ALLOWED_HOSTS[0])

# To handle the android "captive portal" request
def handler500(request):
  res = HttpResponse(status=302)
  res['Location'] = captivePortalUrl
  return res

def handler400(request, exc):
  res = HttpResponse(status=302)
  res['Location'] = captivePortalUrl
  return res

urlpatterns = [
  path('', index, name='index'),
  path('api/chat/', include('chat.urls')),
  path('api/files/', include('files.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
