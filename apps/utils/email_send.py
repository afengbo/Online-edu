#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: '2018/08/17 19:16'

from random import Random

from django.core.mail import send_mail
from django.conf import settings

from apps.users.models import EmailVerifyRecord


def random_str(length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_count = len(chars) - 1
    random = Random()
    for i in range(length):
        str+=chars[random.randint(0, len_count)]
    return str


def send_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        random_code = random_str(6)
    else:
        random_code = random_str(16)
    email_record.code = random_code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "Fone在线网"
        email_body = "请点击以下链接激活你的账号：\n http://127.0.0.1:8000/active/%s" % random_code
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

        if send_status:
            print('Send email succeed!')

    elif send_type == 'forget':
        email_title = "Fone在线网"
        email_body = "请点击以下链接修改你的密码：\n http://127.0.0.1:8000/reset/%s" % random_code
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

        if send_status:
            print('Send email succeed!')

    elif send_type == 'update_email':
        email_title = "Fone在线网"
        email_body = "个人中心修改邮箱验证码为：%s" % random_code
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

        if send_status:
            print('Send email succeed!')
