# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
import datetime
import time
# import json
# import urllib, urllib2
# from auth.auth2 import *
from django.template import RequestContext
from mysite import settings
from django.db import transaction
from django.core.mail import send_mail, BadHeaderError, EmailMessage, EmailMultiAlternatives
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib import messages
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.core import serializers
import json

lock_msg = 'Доступ до сайту тимчасово заблоковано адміністратором'


def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)
        if not request.user.has_perm('ambulat.login_to_site'):
            logout(request)
            messages.add_message(request, messages.INFO, lock_msg)
            return HttpResponseRedirect(settings.LOGIN_URL)
        if not request.user.groups.filter(name=u'Лікар') and request.path == '/ambulat/':
            return HttpResponseRedirect('/ambulat/patient/')
        return view(request, *args, **kwargs)
    return new_view


def get_initials(first_name, middlename):
    try:
        return first_name.title()[0] + '. ' + middlename.title()[0] + '.'
    except IndexError:
        raise


def get_user_initials(user):
    global user_error
    user_error = None	
    user_initials = ''
    try:
        up = get_user_profile(user)
        user_initials = get_initials(user.first_name, up.middlename)
    except UserProfile.DoesNotExist:
        user_error = '- не найден профиль пользавателя'
    except IndexError:
        user_error = '- не указано имя или отчество'
    return user_initials


def ambulatory_maps(request):
    dict_params = {
        'user_initials': get_user_initials(request.user),
        'user_error': user_error
    }
    return render_to_response(
        'ambulat/ambulat.html', 
        dict_params,
        context_instance=RequestContext(request)  # not (1.11)
    )


def load_ambcard(request):
    # amb = Ambcard.objects.all()
    # assert False, amb

    dict_rows = None
    if 'ambcard' in request.GET and request.GET['ambcard']:
        dict_rows = get_ambulatorycards()
    if 'person' in request.GET and request.GET['person']:
        dict_rows = get_personnel()
        # to_json = json.dumps(dict_rows)  # serializers.serialize('json', dict_rows)
        # assert False, to_json
    if 'personid' in request.GET and request.GET['personid']:
        dict_rows = get_curriculum(request.GET['personid'])
    if 'newperson' in request.GET and request.GET['newperson']:
        dict_rows = get_new_curriculum()
    if 'dpersonid' in request.GET and request.GET['dpersonid']:
        dict_rows = get_curriculumdet(request.GET['dpersonid'])

    dict_grid = {
        'total': len(dict_rows),
        'rows': dict_rows
    }

    jresponse = JsonResponse(dict_grid)
    return HttpResponse(jresponse)


def dict_personnel(request):
    dict_spec = Speciality.objects.all().values()
    # dict_spec = [x for x in dict_spec]
    dict_params = {
        'user_initials': get_user_initials(request.user),
        'specialities': dict_spec,
        'user_error': user_error
    }
    return render_to_response(
        'ambulat/personnel.html', 
        dict_params,
        context_instance=RequestContext(request)  # not (1.11)
    )


# procedure not use
def load_personnel(request):
    dict_rows = None
    if 'person' in request.GET and request.GET['person']:
        dict_rows = Personnel.objects.select_related().all().values()
        dict_rows = [x for x in dict_rows]
        for x in dict_rows:
            x['recepttimestart'] = x['recepttimestart'].strftime("%H:%M")
            x['recepttimeend'] = x['recepttimeend'].strftime("%H:%M")

    dict_grid = {
        'total': len(dict_rows),
        'rows': dict_rows
    }

    jresponse = JsonResponse(dict_grid)
    return HttpResponse(jresponse)


@transaction.atomic
def save_personnel(request):
    if request.method == 'POST':
        params = eval(request.POST['id'])
        if params['id'] == 0:
          pers = Personnel(lastname=request.POST['lastname'],
                           firstname=request.POST['firstname'],
                           middlename=request.POST['middlename'],
                           speciality_id=request.POST['speciality_id'],
                           phone=request.POST['phone'],
                           cabinetno=request.POST['cabinetno'])
        else:
          pers = Personnel.objects.get(id=params['id'])
          pers.lastname = request.POST['lastname']
          pers.firstname = request.POST['firstname']
          pers.middlename = request.POST['middlename']
          pers.speciality_id = request.POST['speciality_id']
          pers.phone = request.POST['phone']
          pers.cabinetno = request.POST['cabinetno']
        pers.save()

        curriculum = eval(request.POST['curriculum'])
        if len(curriculum) > 0:
          if params['id'] > 0:
            personnel_id = params['id']
            Curriculum.objects.filter(personnel_id=personnel_id).delete()
          else:
            personnel_id = pers.id

          CurriculumDet.objects.filter(personnel_id=personnel_id).delete()
          for key in curriculum:
            timestart = curriculum[key]['recepttimestart']
            if timestart is not None:
              timestart = datetime.datetime.strptime('01.01.2000 '+timestart, '%d.%m.%Y %H:%M')
            timeend = curriculum[key]['recepttimeend']
            if timeend is not None:
              timeend = datetime.datetime.strptime('01.01.2000 '+timeend, '%d.%m.%Y %H:%M')

            culm = Curriculum(personnel_id=personnel_id,
                              weekday=curriculum[key]['weekday'],
                              recepttimestart=timestart,
                              recepttimeend=timeend)
            culm.save()

            if timestart is not None and timeend is not None:
              delta = datetime.timedelta(minutes=45)
              while timestart < timeend:
                culmd = CurriculumDet(personnel_id=personnel_id,
                                      weekday=curriculum[key]['weekday'],
                                      receptiontime=timestart)
                culmd.save()
                timestart += delta

        return HttpResponse('ok')


@transaction.atomic
def del_personnel(request):
    if request.method == 'POST' and request.POST['personid']:
        Curriculum.objects.filter(personnel_id=request.POST['personid']).delete()
        Personnel.objects.filter(id=request.POST['personid']).delete()
    return HttpResponse('ok')


def select_doctor(request):
    try:
        up = get_user_profile(request.user)
        p = Patient.objects.get(id=up.patientid)
    except ValueError:
        raise Http404()
    except UserProfile.DoesNotExist:
        raise Http404()
    except Patient.DoesNotExist:
        raise Http404('Страница не найдена')

    dict_params = {
        'patient_initials': p,
        'patient_id': p.id,
        'patient_errors': ''
    }
    return render_to_response(
        'patient/seldoctor.html',
        dict_params,
        context_instance=RequestContext(request)  # not (1.11)
    )


def save_ambcard(request):
    if request.method == 'POST':
        # subject, from_email, to_email = 'hello3', 'tigerboy777@mail.ru', 'bvladlen777@gmail.com'
        # message = 'This is an important message.'
        # email = EmailMessage(subject, message, from_email, [to_email])
        # email.attach_file('c:/djcode/mysite/mysite/static/images/netagents_20160529235239.pdf')

        receptiondate = datetime.datetime.strptime(request.POST['receptiondate'], '%d.%m.%Y')
        timestart = datetime.datetime.strptime('01.01.2000 '+request.POST['recepttimestart'], '%d.%m.%Y %H:%M')
        try:
            p = Ambcard.objects.get(personnel_id=request.POST['personnel_id'],
                                    patient_id=request.POST['patient_id'],
                                    receptiondate=receptiondate,
                                    recepttimestart=timestart)
        except Ambcard.DoesNotExist:
            delta = datetime.timedelta(minutes=15)
            acard = Ambcard(personnel_id=request.POST['personnel_id'],
                            patient_id=request.POST['patient_id'],
                            receptiondate=receptiondate,
                            cabinetno=request.POST['cabinetno'],
                            recepttimestart=timestart,
                            recepttimeend=timestart+delta)
            acard.save()
            if settings.SEND_EMAIL_PATIENT and request.user.email:
                subject, from_email, to_email = 'Запис до лікаря', 'bvladlen777@gmail.com', request.user.email
                pers = Personnel.objects.get(id=request.POST['personnel_id'])
                message = 'Ви записані на прийом до лікаря %s, кабінет %s на %s час %s' % \
                          (pers.__str__(), pers.cabinetno,
                           request.POST['receptiondate'],
                           request.POST['recepttimestart'])
                try:						  
                    send_mail(subject, message, from_email, [to_email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found for send mail')
        return HttpResponse('ok')


def doc_view(request):
    path_file = settings.BASE_DIR + '/path/to/Rules_Grawe_2013.pdf'
    try:
        doc = open(path_file, 'rb')
    except IOError:
        response = HttpResponse('Не вдалося відкрити файл!')
    else:
        response = HttpResponse(doc.read(), content_type='application/pdf')  # /msword or /vnd.ms-word
        response['Content-Disposition'] = 'inline; filename=some_file.pdf'
        doc.close()
    return response


def get_currentdate():
    now_date = datetime.date.today()
    return '%02d.%02d.%d' % (now_date.day, now_date.month, now_date.year)


def get_filename_pdf(prefix):
    dt = datetime.datetime.now()
    return '%s_%d%02d%02d%02d%02d%02d.pdf' % (prefix, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def rep_ambulats_pdf(request):
    dict_ambulats = get_ambulatorycards()
    response = PDFTemplateResponse(request, 'ambulat/report/rep_ambulat.html',
                                   {'currentdate': get_currentdate(), 'ambulats': dict_ambulats},
                                   show_content_in_browser=True)
    response['Content-Disposition'] = 'inline; filename="%s"' % (get_filename_pdf('ambulats'))  # attachment
    return response
