# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
import time
from django.template import RequestContext
from mysite import settings
from django.db import transaction
from ambulat.models import *
from policlinic.models import *

def login_patient(request):
    return render_to_response(
        'policlinic/login.html', 
        context_instance=RequestContext(request)
    )

@transaction.atomic
def save_patient(request):
    if request.method == 'POST':
        birthdaydt = datetime.datetime.strptime(request.POST['birthday'], '%d.%m.%Y')
        try:
            p = Patient.objects.get(lastname = request.POST['lastname'],
                                    firstname = request.POST['firstname'],
                                    middlename = request.POST['middlename'],
                                    birthday = birthdaydt)
        except Patient.DoesNotExist:
            p = Patient(lastname = request.POST['lastname'],
                        firstname = request.POST['firstname'],
                        middlename = request.POST['middlename'],
                        birthday = birthdaydt)
            p.save()
            Patient.objects.filter(id=p.id).update(cardno=str(100000+p.id))
    return HttpResponse(p.id)

def select_doctor(request, patient_id):
    try:
        patient_id = int(patient_id)
        p = Patient.objects.get(id=patient_id)
    except ValueError:
        raise Http404()
    except Patient.DoesNotExist:
        raise Http404()

    dict_params = {
        'patient_initials': p,
        'patient_id': p.id,
        'patient_errors': ''
    }
    return render_to_response(
        'policlinic/seldoctor.html',
        dict_params,
        context_instance=RequestContext(request)
    )

def load_policlinic(request):
    dict_rows = None
    if 'person' in request.GET and request.GET['person']:
        dict_rows = get_personnel()
    if 'personid' in request.GET and request.GET['personid']:
        dict_rows = get_curriculumdet(request.GET['personid']);

    dict_grid = {
        'total': len(dict_rows),
        'rows': dict_rows
    }

    jresponse = JsonResponse(dict_grid)
    return HttpResponse(jresponse)

def save_ambcard(request):
    if request.method == 'POST':
        receptiondate = datetime.datetime.strptime(request.POST['receptiondate'], '%d.%m.%Y')
        timestart = datetime.datetime.strptime('01.01.2000 '+request.POST['recepttimestart'], '%d.%m.%Y %H:%M')
        delta = datetime.timedelta(minutes=15)
        acard = Ambcard(personnel_id=request.POST['personnel_id'],
                        patient_id=request.POST['patient_id'],
                        receptiondate=receptiondate,
                        cabinetno=request.POST['cabinetno'],
                        recepttimestart=timestart,
                        recepttimeend=timestart+delta)
        acard.save()
        return HttpResponse('ok')

