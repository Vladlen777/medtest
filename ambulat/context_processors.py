# -*- coding: utf-8 -*-
from django.core.context_processors import request
# from django.template.context_processors import request
from .apps import *


def menu(request):
    return {
        "ambmenu": {
              1: {"name": "Прийом пацієнтів", "url": "/ambulat/"},
              2: {"name": "Персонал", "url": "/ambulat/personnel/"},
              3: {"name": "Спеціальності", "url": "#spec"},
              4: {"name": "Про програму", "url": "#about"},
              5: {"name": "Вихід", "url": "/ambulat/logout/"}
        },
        "patientmenu": {
              1: {"name": "Про програму", "url": "#about"},
              2: {"name": "Вихід", "url": "/ambulat/logout/"}
        },
        "ambulatapp": AmbulatAppConfig.verbose_name,
    }
