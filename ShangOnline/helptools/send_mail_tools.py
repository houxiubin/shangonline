from random import randint
from ShangOnline.settings import EMAIL_FROM
from django.core.mail import send_mail

from users.models import EmailVerify


def get_code(code_length=8):
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    code = ''
    for i in range(code_length):
        code += code_source[randint(0, len(code_source) - 1)]
    return code


def send_email_verify(email, send_type):
    code = get_code()
    if send_type == 'changeemail':
        code = get_code(4)
    email_ver = EmailVerify()
    email_ver.email = email
    email_ver.code = code
    email_ver.send_type = send_type
    email_ver.save()

    if send_type == 'register':
        send_title = '欢迎注册尚在线教育:'
        send_body = '请点以下链接以激活\n http://127.0.0.1:8000/users/active/' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 'forget':
        send_title = '欢迎登录尚在线教育'
        send_body = '请点以下链接以更改密码\n http://127.0.0.1:8000/users/reset/' + code + '/' + email
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 'changeemail':
        send_title = '欢迎更改邮箱'
        send_body = '请复制以下验证码到更改框中：\n ' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])
