from django.db import models
from django.http import JsonResponse
from django.db import connection
from django.shortcuts import _get_queryset
from mysite import settings
# import cx_Oracle
from mysql.connector import Error  # MySQLConnection, Error


def dictfetchall(cursor):
    # Returns all rows from a cursor as a dict
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

'''
def get_connection(db_name):
    my_connection = None
    try:
        db = settings.DATABASES[db_name]
        my_connection = cx_Oracle.connect('%s/%s@%s' % (db['USER'],db['PASSWORD'],db['NAME']))
    except cx_Oracle.DatabaseError, info:
        print "Logon  Error:", info
    return my_connection
'''


def get_json_or_dict(text_sql, is_query=True, connect=connection, only_dict=True):
    my_cursor = connect.cursor()
    try:
        if is_query:
            my_cursor.execute(text_sql)
        else:
            my_cursor.callproc(text_sql)
        dict_data = dictfetchall(my_cursor)
    except Error as e:
        dict_data = []
        print(e)
    finally:
        my_cursor.close()
        connect.close()
    return dict_data if only_dict else JsonResponse(dict_data, safe=False)


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
