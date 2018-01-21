# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
from mysite.models import *

def get_curriculumdet(personnel_id):
    return get_json_or_dict('''
		SELECT t.id, t.curriculumdate, t.weekday, t.receptiontime, coalesce(ac.ambid,0) ambid
		  FROM (
        SELECT c.id, DATE_FORMAT(a.curriculumdate, '%d.%m.%Y') curriculumdate,
               CASE c.weekday
                    WHEN 0 THEN 'Понедельник'
                    WHEN 1 THEN 'Вторник'
                    WHEN 2 THEN 'Среда'
                    WHEN 3 THEN 'Четрверг'
                    WHEN 4 THEN 'Пятница'
                    WHEN 5 THEN 'Суббота'
                    WHEN 6 THEN 'Воскресенье'
               END weekday,		
               TIME_FORMAT(c.receptiontime,'%H:%i') receptiontime,
			   c.personnel_id,
			   a.curriculumdate rdate,
			   c.receptiontime rtime
          FROM (		 
        SELECT DATE_ADD(CURDATE(), INTERVAL (@row_number:=@row_number + 1) DAY) curriculumdate,
               WEEKDAY(DATE_ADD(CURDATE(), INTERVAL @row_number DAY)) weekday
          FROM (SELECT 0 id UNION
                SELECT 1 id UNION
                SELECT 2 id UNION
                SELECT 3 id UNION
                SELECT 4 id UNION
                SELECT 5 id UNION
                SELECT 6 id) c, 
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
		ORDER BY t.rdate, t.rtime''',
        connection,
        only_dict=True,
        eprlogin_second=False
    )
