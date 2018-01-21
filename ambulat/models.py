# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# from django.http import JsonResponse
from django.db import connection
# from mysite import settings
from mysite.models import *
# import time
import datetime
# from mysql.connector import MySQLConnection, Error
# from python_mysql_dbconfig import read_db_config


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'Користувач')    
    middlename = models.CharField(verbose_name=u'По батькові', max_length=30, default='', blank=True)
    birthday = models.DateField(verbose_name=u'День народження', null=True, blank=True)
    phone = models.CharField(verbose_name=u'Телефон', max_length=32, blank=True)
    website = models.URLField(verbose_name=u'Сайт', blank=True)
    icq = models.CharField(verbose_name=u'ICQ', max_length=32, blank=True)
    skype = models.CharField(verbose_name=u'Skype', max_length=32, blank=True)
    patientid = models.IntegerField(verbose_name=u'Код пацієнта', null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.user.last_name, self.user.first_name, self.middlename)

    class Meta:
        verbose_name = u'Профіль користувача'
        verbose_name_plural = u'Профілі користувачей'
        permissions = (
            ('login_to_site', u'Вхід до сайту'),
        )


class Speciality(models.Model):
    name = models.CharField(verbose_name=u'Назва', max_length=50, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Спеціальність'
        verbose_name_plural = u'Спеціальності'


class PersonnelManager(models.Manager):
    @staticmethod
    def get_personnel_all():
        return get_json_or_dict('sp_personnel_all', is_query=False)


class Personnel(models.Model):  
    lastname = models.CharField(verbose_name=u'Прізвище', max_length=30, blank=False)
    firstname = models.CharField(verbose_name=u"И'мя", max_length=30, blank=False)
    middlename = models.CharField(verbose_name=u'По батькові', max_length=30, default='', blank=True)
    speciality = models.ForeignKey(Speciality, unique=False, db_index=True, verbose_name=u'Спеціальність')
    phone = models.CharField(verbose_name=u'Телефон', max_length=32, default='', blank=True)
    cabinetno = models.IntegerField(verbose_name=u'Кабінет', blank=False)
    objects = PersonnelManager()

    def __str__(self):
        return '%s %s. %s. - %s' % (self.lastname, 
                                    self.firstname.title()[0], 
                                    self.middlename.title()[0],
                                    self.speciality.name)

    class Meta:
        verbose_name = u'Фахівець'
        verbose_name_plural = u'Персонал'


class Curriculum(models.Model):
    personnel = models.ForeignKey(Personnel, unique=False, db_index=True, verbose_name=u'Фахівець')
    weekday = models.IntegerField(verbose_name=u'День тиждня', blank=False)
    recepttimestart = models.DateTimeField(verbose_name=u'Час прийому з', null=True, blank=True)
    recepttimeend = models.DateTimeField(verbose_name=u'Час прийому по', null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.personnel, self.weekday)

    class Meta:
        verbose_name = u'Розклад фахівця'
        verbose_name_plural = u'Розклад персонала'


class CurriculumDet(models.Model):
    personnel = models.ForeignKey(Personnel, unique=False, db_index=True, verbose_name=u'Фахівець')
    weekday = models.IntegerField(verbose_name=u'День тиждня', blank=False)
    receptiontime = models.DateTimeField(verbose_name=u'Час прийому', blank=False)

    def __str__(self):
        return '%s %s' % (self.personnel, self.weekday)

    class Meta:
        verbose_name = u'Розклад детально'
        verbose_name_plural = u'Розклад детально'


class Patient(models.Model):  
    lastname = models.CharField(verbose_name=u'Прізвище', max_length=30, blank=False)
    firstname = models.CharField(verbose_name=u"И'мя", max_length=30, blank=False)
    middlename = models.CharField(verbose_name=u'По батькові', max_length=30, default='', blank=True)
    birthday = models.DateField(verbose_name=u'День народження', null=True, blank=True)
    address = models.CharField(verbose_name=u'Адреса', max_length=80, blank=True)
    workplace = models.CharField(verbose_name=u'Місце роботи', max_length=50, blank=True)
    cardno = models.CharField(verbose_name=u'Номер карти', max_length=10, unique=True, blank=False)

    def __str__(self):
        return '%s %s. %s.' % (self.lastname, self.firstname.title()[0], self.middlename.title()[0])

    class Meta:
        verbose_name = u'Паціент'
        verbose_name_plural = u'Паціенти'


class Ambcard(models.Model):
    personnel = models.ForeignKey(Personnel, unique=False, db_index=True, verbose_name=u'Фахівець')  
    patient = models.ForeignKey(Patient, unique=False, db_index=True, verbose_name=u'Паціент')
    receptiondate = models.DateField(verbose_name=u'Дата прийому', null=False, blank=False)
    cabinetno = models.IntegerField(verbose_name=u'Кабінет', null=True, blank=True)
    periodcure = models.CharField(verbose_name=u'Період лікування', max_length=30, blank=True)
    prescriptmedicine = models.CharField(verbose_name=u'Призначення ліків', max_length=50, blank=True)
    symptoms = models.CharField(verbose_name=u'Симптоми', max_length=100, blank=True)
    weight = models.DecimalField(verbose_name=u'Вага', max_digits=4, decimal_places=1, null=True, blank=True)
    pressure = models.CharField(verbose_name=u'Тиск', max_length=30, blank=True)
    analysis = models.CharField(verbose_name=u'Аналізи та результати', max_length=100, blank=True)
    startdiagnosis = models.CharField(verbose_name=u'Попередній діагноз', max_length=100, blank=True)
    enddiagnosis = models.CharField(verbose_name=u'Остаточний діагноз', max_length=100, blank=True)
    recepttimestart = models.DateTimeField(verbose_name=u'Час прийому з', default=datetime.datetime.now, blank=False)
    recepttimeend = models.DateTimeField(verbose_name=u'Час прийому по', default=datetime.datetime.now, blank=False)

    def __str__(self):
        return '№%s %s %s' % (self.patient.cardno, self.patient.lastname, self.receptiondate)

    class Meta:
        unique_together = ('personnel', 'receptiondate', 'recepttimestart')
        verbose_name = u'Амбулаторна карта'
        verbose_name_plural = u'Амбулаторні карти'


def get_user_profile(user):
    try:
        return UserProfile.objects.get(user_id=user.id)
    except UserProfile.DoesNotExist:
        raise


def get_ambulatorycards():
    return get_json_or_dict('''
        SELECT a.id ambid, CONCAT(pl.lastname,' ',pl.firstname,' ',pl.middlename) doctorfullname,
               DATE_FORMAT(a.receptiondate,'%d.%m.%Y') receptiondate, a.cabinetno, 
               CONCAT(p.lastname,' ',p.firstname,' ',p.middlename) patientfullname, p.cardno,
               a.periodcure, a.prescriptmedicine, a.symptoms, a.weight, a.pressure, a.analysis,
               a.startdiagnosis, a.enddiagnosis, s.name specialityname, 
               p.birthday, p.address, p.workplace, 
               TIME_FORMAT(a.recepttimestart,'%H:%i') recepttimestart, 
               TIME_FORMAT(a.recepttimeend,'%H:%i') recepttimeend			   
          FROM ambulat_ambcard a,
               ambulat_personnel pl,
               ambulat_speciality s,
               ambulat_patient p
         WHERE a.personnel_id = pl.id
           AND pl.speciality_id = s.id
           AND a.patient_id = p.id
        ''')


def get_personnel_test():
    my_cursor = connection.cursor()
    try:
        my_cursor.callproc('PersonnelList')
        dict_data = dictfetchall(my_cursor)
    except Error as e:
        dict_data = []
        print(e)
    finally:
        my_cursor.close()
        connection.close()
    return dict_data


def get_personnel2():
    specialities = Speciality.objects.all().values("id", "name")
    specialities_info = {}
    for speciality in specialities:
        specialities_info[speciality["id"]] = speciality["name"]
    doctors = Personnel.objects.all().values("id", "lastname", "firstname", "middlename", "speciality_id",
                                             "phone", "cabinetno")

    for doctor in doctors:
        doctor["personnelfullname"] = "%s %s %s" % (doctor["lastname"], doctor["firstname"], doctor["middlename"])
        doctor["specialityname"] = specialities_info[doctor["speciality_id"]]
    return doctors


def get_personnel():
    return Personnel.objects.get_personnel_all()


def get_curriculum(personnel_id):
    return get_json_or_dict('''
        SELECT c.id, DATE_FORMAT(a.curriculumdate, '%d.%m.%Y') curriculumdate,
               c.weekday weekdaynum,
               get_weekday(c.weekday) weekday,
               TIME_FORMAT(c.recepttimestart,'%H:%i') recepttimestart, 
               TIME_FORMAT(c.recepttimeend,'%H:%i') recepttimeend		
          FROM (
        SELECT DATE_ADD(CURDATE(), INTERVAL (@row_number:=@row_number + 1) DAY) curriculumdate,
               WEEKDAY(DATE_ADD(CURDATE(), INTERVAL @row_number DAY)) weekday
          FROM (SELECT id FROM vweekdays) c, 
               (SELECT @row_number:=-1) t
        ) a,
        ambulat_curriculum c
		WHERE c.personnel_id = ''' + personnel_id + '''
          AND a.weekday = c.weekday
        ORDER BY a.curriculumdate;
        ''')


def get_new_curriculum():
    return get_json_or_dict('''
        SELECT null id, DATE_FORMAT(a.curriculumdate, '%d.%m.%Y') curriculumdate,
               a.weekday weekdaynum,
               get_weekday(a.weekday) weekday,
               null recepttimestart, 
               null recepttimeend		
          FROM (
        SELECT DATE_ADD(CURDATE(), INTERVAL (@row_number:=@row_number + 1) DAY) curriculumdate,
               WEEKDAY(DATE_ADD(CURDATE(), INTERVAL @row_number DAY)) weekday
          FROM (SELECT id FROM vweekdays) c, 
               (SELECT @row_number:=-1) t
        ) a
        ORDER BY a.curriculumdate
        ''')


def get_curriculumdet(personnel_id):
    return get_json_or_dict('''
        SELECT t.id, t.curriculumdate, t.weekday, t.receptiontime, coalesce(ac.ambid,0) ambid
          FROM (
        SELECT c.id, DATE_FORMAT(a.curriculumdate, '%d.%m.%Y') curriculumdate,
               get_weekday(a.weekday) weekday,		
               TIME_FORMAT(c.receptiontime,'%H:%i') receptiontime,
               c.personnel_id, a.curriculumdate rdate, c.receptiontime rtime
          FROM (		 
        SELECT DATE_ADD(CURDATE(), INTERVAL (@row_number:=@row_number + 1) DAY) curriculumdate,
               WEEKDAY(DATE_ADD(CURDATE(), INTERVAL @row_number DAY)) weekday
          FROM (SELECT id FROM vweekdays) c, 
               (SELECT @row_number:=-1) t
        ) a,
        ambulat_curriculumdet c	
        WHERE a.weekday = c.weekday
		  AND c.personnel_id = '''+personnel_id+''' ) t 
        LEFT JOIN
        (SELECT id ambid, personnel_id, receptiondate rdate, recepttimestart rtime
           FROM ambulat_ambcard
          WHERE personnel_id = '''+personnel_id+'''
            AND receptiondate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 6 DAY)) ac
        ON t.personnel_id = ac.personnel_id
            AND t.rdate = ac.rdate
            AND t.rtime = ac.rtime
        ORDER BY t.rdate, t.rtime''')


def get_user_profile_id(last_name, first_name, middlename, birthday):
    up_id = get_json_or_dict('''
        SELECT up.id
          FROM auth_user u,
               ambulat_userprofile up
         WHERE u.id = up.user_id
           AND u.last_name = "'''+last_name+'''"
           AND u.first_name = "'''+first_name+'''"
           AND up.middlename = "'''+middlename+'''"
           AND up.birthday = DATE_FORMAT("'''+birthday+'''", '%Y-%m-%d')
        ''')
    return up_id[0]['id'] if up_id else 0
