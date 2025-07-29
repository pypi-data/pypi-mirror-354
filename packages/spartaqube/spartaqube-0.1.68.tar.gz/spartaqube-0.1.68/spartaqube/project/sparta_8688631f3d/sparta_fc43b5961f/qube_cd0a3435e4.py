import os
import json
import uuid
import base64
import random
import string
from datetime import datetime
import hashlib
import requests
import hashlib
from cryptography.fernet import Fernet
from random import randint
import pytz
UTC = pytz.utc
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth.hashers import make_password
from django.conf import settings as conf_settings
from django.contrib.auth import login
from project.models import UserProfile, Avatar, contactUS, SpartaQubeCode
from project.sparta_8688631f3d.sparta_07864420ce import qube_7bd77509b9 as qube_7bd77509b9
from project.sparta_8688631f3d.sparta_a9eedb9d32.qube_60d1e416df import Email as Email
from project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d import sparta_6ae4813892, sparta_23d9373307, sparta_10f2573ca7
from project.sparta_8688631f3d.sparta_227f7b5cfa.qube_bd5e6b73de import sparta_412803c509
from project.logger_config import logger


def sparta_aed4a1d8ba(json_data, user_obj):
    """
    Send an email and contact SpartaQuant help desk
    """
    message = json_data['messageContactUs']
    title = json_data['titleContactUs']
    captcha = json_data['captcha']
    dateNow = datetime.now()
    contactUS.objects.create(message=message, title=title, user=user_obj,
        date_created=dateNow)
    json_data_dict = {'message': message, 'title': title, 'captcha':
        captcha, 'email': user_obj.email, 'first_name': user_obj.first_name,
        'last_name': user_obj.last_name}
    json_data_post = dict()
    json_data_post['jsonData'] = json.dumps(json_data_dict)
    proxies_dict = {'http': os.environ.get('http_proxy', None), 'https': os.environ.get('https_proxy', None)}
    response = requests.post(
        f'{conf_settings.SPARTAQUBE_WEBSITE}/contact-us-app', data=json.dumps(json_data_post), proxies=proxies_dict)
    if response.status_code == 200:
        try:
            logger.debug('response.text')
            logger.debug(response.text)
            json_data = json.loads(response.text)
            return json_data
        except Exception as e:
            return {'res': -1, 'errorMsg': str(e)}
    res = {'res': -1, 'errorMsg':
        'An unexpected error occurred, please check your internet connection and try again'
        }
    return res


def sparta_343911d737(message, typeCase=0, companyName=None):
    """
    
    """
    admin_user_set = User.objects.filter(is_staff=True)
    if admin_user_set.count() > 0:
        admin_user_obj = admin_user_set[0]
        emailObj = Email(admin_user_obj.username, [conf_settings.CONTACT_US_EMAIL], 'Contact US', 'Contact US new message')
        if companyName is not None:
            emailObj.addOneRow('Company', companyName)
            emailObj.addLineSeparator()
        emailObj.addOneRow('Message', message)
        emailObj.addLineSeparator()
        if int(typeCase) == 0:
            emailObj.addOneRow('Type', 'General question')
        else:
            emailObj.addOneRow('Type', 'Report Bug')
        emailObj.send()


def sparta_3e080a6378(json_data, userObj):
    """
    Update the password
    """
    password = json_data['password']
    passwordConfirm = json_data['passwordConfirm']
    oldPassword = json_data['oldPassword']
    if len(password) > 4:
        if password == passwordConfirm:
            if userObj.check_password(oldPassword):
                passwordEnc = make_password(password)
                userObj.password = passwordEnc
                userObj.save()
                res = {'res': 1, 'userObj': userObj}
            else:
                res = {'res': -1, 'message':
                    'The current password is not correct'}
        else:
            res = {'res': -1, 'message': 'Please put the same passwords'}
    else:
        res = {'res': -1, 'message': 'Password must be at least 5 characters'}
    return res


def sparta_fdbd3ad20a(json_data, userObj):
    """
        Pre-check passwords inputs
    """
    password = json_data['password']
    passwordConfirm = json_data['passwordConfirm']
    oldPassword = json_data['oldPassword']
    if len(password) > 4:
        if password == passwordConfirm:
            if userObj.check_password(oldPassword):
                res = {'res': 1}
            else:
                res = {'res': -1, 'message':
                    'The current password is not correct'}
        else:
            res = {'res': -1, 'message': 'Please put the same passwords'}
    else:
        res = {'res': -1, 'message': 'Password must be at least 5 characters'}
    return res


def sparta_6be0e12d94(json_data, userObj) ->dict:
    """
    Update the spartaqube code
    """
    old_spartaqube_code = json_data['old_spartaqube_code']
    new_spartaqube_code = json_data['new_spartaqube_code']
    if not sparta_412803c509(old_spartaqube_code):
        return {'res': -1, 'errorMsg': 'Invalid current code'}
    key = hashlib.md5(new_spartaqube_code.encode('utf-8')).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    key = key.decode('utf-8')
    date_now = datetime.now().astimezone(UTC)
    spartaqube_code_set = SpartaQubeCode.objects.all()
    if spartaqube_code_set.count() == 0:
        SpartaQubeCode.objects.create(spartaqube_code=key, date_created=
            date_now, last_update=date_now)
    else:
        spartaqube_code_obj = spartaqube_code_set[0]
        spartaqube_code_obj.spartaqube_code = key
        spartaqube_code_obj.last_update = date_now
        spartaqube_code_obj.save()
    return {'res': 1}


def sparta_dab3f1afab(json_data, userObj):
    """
    Update the image profile
    """
    base64image = json_data['base64image']
    hs = hashlib.sha256((str(userObj.id) + '_' + userObj.email + str(
        datetime.now())).encode('utf-8')).hexdigest()
    _format, _img_str = base64image.split(';base64,')
    _name, ext = _format.split('/')
    name = _name.split(':')[-1]
    user_profile_obj = UserProfile.objects.get(user=userObj)
    dateNow = datetime.now()
    avatar_obj = Avatar.objects.create(avatar=name, image64=_img_str,
        date_created=dateNow)
    user_profile_obj.avatar = avatar_obj
    user_profile_obj.save()
    res = {'res': 1}
    return res


def sparta_83812ae9b4(json_data, userObj):
    """
    Change dark/light theme
    """
    is_dark_theme = json_data['bDarkTheme']
    user_profile_obj = UserProfile.objects.get(user=userObj)
    user_profile_obj.is_dark_theme = is_dark_theme
    user_profile_obj.save()
    res = {'res': 1}
    return res


def sparta_bc0154ba4c(json_data, userObj):
    """
    Change code editor theme
    """
    theme = json_data['theme']
    user_profile_obj = UserProfile.objects.get(user=userObj)
    user_profile_obj.editor_theme = theme
    if 'fontSizePx' in json_data:
        try:
            user_profile_obj.font_size = float(json_data['fontSizePx'])
        except:
            pass
    user_profile_obj.save()
    res = {'res': 1}
    return res


def sparta_52f4735e0b() ->str:
    """
    Get encryption key to ask to the master node token
    """
    keygen_fernet = 'spartaqube-reset-password'
    key = keygen_fernet.encode('utf-8')
    key = hashlib.md5(key).hexdigest()
    key = base64.b64encode(key.encode('utf-8'))
    return key.decode('utf-8')


def sparta_37cc11c58c(json_data):
    """
    Reset user password (we need the admin password for that)
    """
    email = json_data['email']
    admin_password = json_data['admin']
    new_password = json_data['new_password']
    new_password_confirm = json_data['new_password_confirm']
    if not sparta_10f2573ca7(admin_password):
        return {'res': -1, 'errorMsg': 'Invalid spartaqube admin password'}
    if not User.objects.filter(username=email).exists():
        return {'res': -1, 'errorMsg': 'Invalid email'}
    if new_password != new_password_confirm:
        return {'res': -1, 'errorMsg': 'Passwords must be the same'}
    user_obj = User.objects.filter(username=email).all()[0]
    password_enc = make_password(new_password)
    user_obj.password = password_enc
    user_obj.save()
    return {'res': 1, 'new_password': new_password}


def sparta_4fc18e27f9(json_data):
    """
    DEPRECATED
    """
    captcha = json_data['captcha']
    email = json_data['email']
    admin_password = json_data['admin']
    captcha_validator_dict = sparta_6ae4813892(captcha)
    if captcha_validator_dict['res'] != 1:
        return {'res': -1, 'errorMsg': 'Invalid captcha'}
    if not sparta_23d9373307(admin_password):
        return {'res': -1, 'errorMsg': 'Invalid spartaqube admin password'}
    if not User.objects.filter(username=email).exists():
        return {'res': -1, 'errorMsg': 'Invalid email'}
    user_obj = User.objects.filter(username=email).all()[0]
    user_profile_obj = db_functions.get_user_profile_obj(user_obj)
    token_reset_password_str = ''.join(random.choice(string.ascii_uppercase +
        string.digits) for _ in range(5))
    user_profile_obj.token_reset_password = token_reset_password_str
    user_profile_obj.save()
    return {'res': 1, 'token_reset': token_reset_password_str}


def sparta_62a725473d(request, json_data):
    """
    DEPRECATED
    """
    captcha = json_data['captcha']
    email = json_data['email']
    admin_password = json_data['admin']
    token_reset = json_data['token_reset']
    new_password = json_data['new_password']
    new_password_confirm = json_data['new_password_confirm']
    captcha_validator_dict = sparta_6ae4813892(captcha)
    if captcha_validator_dict['res'] != 1:
        return {'res': -1, 'errorMsg': 'Invalid captcha'}
    if not sparta_23d9373307(admin_password):
        return {'res': -1, 'errorMsg': 'Invalid spartaqube admin password'}
    if not User.objects.filter(username=email).exists():
        return {'res': -1, 'errorMsg': 'Invalid email'}
    if new_password != new_password_confirm:
        return {'res': -1, 'errorMsg': 'Passwords must be the same'}
    user_obj = User.objects.filter(username=email).all()[0]
    user_profile_obj = db_functions.get_user_profile_obj(user_obj)
    if user_profile_obj.token_reset_password != token_reset:
        return {'res': -1, 'errorMsg': 'Invalid reset token'}
    user_profile_obj.token_reset_password = ''
    user_profile_obj.save()
    password_enc = make_password(new_password)
    user_obj.password = password_enc
    user_obj.save()
    login(request, user_obj)
    return {'res': 1}

#END OF QUBE
