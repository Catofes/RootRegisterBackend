# -*- coding: UTF-8 -*-
from bson.objectid import ObjectId
import RUtils
import re
from pymongo import MongoClient
import time


class StudentList:
    def __init__(self, client=MongoClient()):
        self.client = client
        self.db = self.client.register

    def on_get(self, req, resp):
        if 'password' not in req.params.keys():
            raise RUtils.RError(2)
        if req.params['password'] != RUtils.RConfig().password:
            raise RUtils.RError(2)
        data = self.db.students.find({})
        result = []
        for i in data:
            result.append({
                'id': str(i['_id']),
                'name': i['name'],
                'phone': i['phone'],
                'email': i['email'],
                'academy': i['academy'],
                'wechat': i['wechat'],
                'arrive_date': i['arrive_date'],
                'leave_date': i['leave_date'],
                'job': i['job'],
                'special': i['special'],
                'register_time': i['register_time']
            })
        req.context['result'] = result

    def on_post(self, req, resp):
        if 'request' not in req.context.keys():
            raise RUtils.RError(6)
        request = req.context['request']
        # Check Name
        if 'name' not in request.keys():
            raise RUtils.RError(3)
        name = request['name']
        if len(name) > 10:
            raise RUtils.RError(3)
        # Check Phone
        if 'phone' not in request.keys():
            raise RUtils.RError(4)
        phone = request['phone']
        if not re.match('0?(13|14|15|16|17|18)[0-9]{9}', phone):
            raise RUtils.RError(4)
        if self.db.students.find_one({'phone': phone}):
            raise RUtils.RError(8)
        # Check Email
        if 'email' not in request.keys():
            raise RUtils.RError(5)
        email = request['email']
        if not re.match('^[a-z0-9](\w|\.|-)*@([a-z0-9]+-?[a-z0-9]+\.){1,3}[a-z]{2,10}$', email):
            raise RUtils.RError(5)
        if self.db.students.find_one({'email': email}):
            raise RUtils.RError(9)
        # Check School
        if 'academy' not in request.keys():
            raise RUtils.RError(6)
        school = request['academy']
        # Wechat
        wechat = ""
        if 'wechat' in request.keys():
            wechat = request['wechat']
        # Arrive_date
        arrive_date = ""
        if 'arrive_date' in request.keys():
            arrive_date = request['arrive_date']
        # Leave_date
        leave_date = ""
        if 'leave_date' in request.keys():
            leave_date = request['leave_date']
        # Job
        job = ""
        if 'job' in request.keys():
            job = request['job']
        # Special
        special = ""
        if 'special' in request.keys():
            special = request['special']

        if len(self.db.students.find({})) > 100:
            raise RUtils.RError(10)

        register_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.db.students.insert({
            'name': name,
            'phone': phone,
            'email': email,
            'academy': school,
            'wechat': wechat,
            'arrive_date': arrive_date,
            'leave_date': leave_date,
            'job': job,
            'special': special,
            'register_time': register_time
        })
