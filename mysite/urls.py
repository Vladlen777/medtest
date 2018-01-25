"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
# from calculator.views import *
from ambulat.views import *
from django.contrib.auth.views import login, logout 
# from django.contrib.auth import views as auth_views (django 1.11)
from ambulat.admin import my_site
from rest_framework.urlpatterns import format_suffix_patterns

'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
'''

# def my_login_view(request):
#    return auth_views.LoginView.as_view(template_name='ambulat/login.html',
#                                        extra_context={'app_path': request.get_full_path()})(request)

urlpatterns = [
    # url(r'^ambulat/admin/', include(admin.site.urls)),
    url(r'^ambulat/admin/', include(my_site.urls)),
    url(r'^hello/', views.hello),
    url(r'^time/', views.current_datetime),
    url(r'^lisalogin/', views.lisalogin),
    url(r'^lisamain/', views.lisamain),
    # url(r'^search/policylist/', views.policylist),
    # url(r'^lisa/calculator/$', calculator),
    # url(r'^lisa/calculator/rule/$', reload_rule),
    # url(r'^lisa/calculator/addgroup/$', add_group_risk),
    # url(r'^lisa/calculator/calc/', calculate),
    # url(r'^lisa/calculator/calc2/', calculate2),
    url(r'^lisapdf/', views.pdf_view),
    url(r'^ambulat/login/$', login, {'template_name': 'ambulat/login.html'}),  # my_login_view), (1.11)
    url(r'^ambulat/logout/$', logout, {'template_name': 'ambulat/login.html'}),
    url(r'^ambulat/register/$', RegisterFormView.as_view()),
    url(r'^ambulat/$', requires_login(ambulatory_maps)),
    url(r'^ambulat/load/$', requires_login(load_ambcard)),	
    url(r'^ambulat/personnel/$', requires_login(dict_personnel)),
    url(r'^ambulat/personnel/load/$', requires_login(load_ambcard)),
    url(r'^ambulat/personnel/save/$', requires_login(save_personnel)),
    url(r'^ambulat/personnel/del/$', requires_login(del_personnel)),
    url(r'^ambulat/patient/$', requires_login(select_doctor)),
    url(r'^ambulat/patient/load/$', requires_login(load_ambcard)),
    url(r'^ambulat/patient/save/$', requires_login(save_ambcard)),
    url(r'^ambulat/doc/$', requires_login(doc_view)),
    url(r'^ambulat/rep_ambulat/$', requires_login(rep_ambulats_pdf)),
    url(r'^ambulat/speciality/$', SpecialityList.as_view()),
    url(r'^ambulat/speciality/(?P<pk>[0-9]+)/$', SpecialityDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
