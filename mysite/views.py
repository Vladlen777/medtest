# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, Http404
import datetime
# import json
# import urllib, urllib2
# from auth.auth2 import *
from django.template import RequestContext
# from mymenu.models import Menu
from mysite import settings


def hello(request):
    return HttpResponse("Здравствуй мир!!!")


def current_datetime(request):
    now = datetime.datetime.now()
    return render_to_response('current_datetime.html', {'current_date': now})


def lisalogin(request):
    responce = render_to_response('index.html')
    # del_cookies(request, responce)
    return responce


def lisamain(request):
    if 'error' in request.GET and request.GET['error'] == 'access_denied':
        return redirect('http://127.0.0.1:8000/lisalogin')
    # menu_list = Menu.objects.all()
    responce = render_to_response('lisamain.html',
                                  # {'menu': menu_list},
                                  context_instance=RequestContext(request))
    return responce


def pdf_view(request):
    with open('path/to/Rules_Grawe_2013.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed
