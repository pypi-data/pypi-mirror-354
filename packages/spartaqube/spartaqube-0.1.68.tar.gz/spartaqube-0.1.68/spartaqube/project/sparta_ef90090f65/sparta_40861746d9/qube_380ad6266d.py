import os
import socket
import json
import requests
from datetime import date
from datetime import datetime
from project.models import UserProfile, AppVersioning
from django.conf import settings as conf_settings
from spartaqube_app.secrets import sparta_5f33e0d2c4
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.sparta_8688631f3d.sparta_5149e63dd6.qube_0a8e8bbdab import sparta_8c5bc8c8c4
import pytz
UTC = pytz.utc


class dotdict(dict):
    """
    dot.notation access to dictionary attributes
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def sparta_5543508842(appViewsModels):
    """
    
    """
    if isinstance(appViewsModels, list):
        for thisModel in appViewsModels:
            for thisKey in list(thisModel.keys()):
                if isinstance(thisModel[thisKey], date):
                    thisModel[thisKey] = str(thisModel[thisKey])
    else:
        for thisKey in list(appViewsModels.keys()):
            if isinstance(appViewsModels[thisKey], date):
                appViewsModels[thisKey] = str(appViewsModels[thisKey])
    return appViewsModels


def sparta_d071038e8a(thisText):
    """
    
    """
    thisPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    thisPath = thisPath + str('/log/log.txt')
    file1 = open(thisPath, 'a')
    file1.write(thisText)
    file1.writelines('\n')
    file1.close()


def sparta_4ea1ca7fc0(request):
    """
    
    """
    return {'appName': 'Project', 'user': request.user, 'ip_address':
        request.META['REMOTE_ADDR']}


def sparta_72658291d1():
    """
    
    """
    return conf_settings.PLATFORM


def sparta_a193455a5d():
    """
        Return the webpack manifest
    """
    thisPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    thisPath = os.path.dirname(os.path.dirname(thisPath))
    if conf_settings.DEBUG:
        static_path = 'static'
    else:
        static_path = 'staticfiles'
    pathFile = thisPath + f'/{static_path}/dist/manifest.json'
    f = open(pathFile)
    manifest = json.load(f)
    if conf_settings.B_TOOLBAR:
        manifestKey = list(manifest.keys())
        for thisKey in manifestKey:
            manifest[thisKey] = thisPath + f'/{static_path}' + manifest[thisKey
                ]
    return manifest


def sparta_f8c7f58a23(request):
    """
    These are global variables we need to send for each view (render(request, 'file.html', dictVar))    
    """
    urlPrefix = ''
    wsPrefix = ''
    if len(urlPrefix) > 0:
        urlPrefix = '/' + str(urlPrefix)
    if len(wsPrefix) > 0:
        wsPrefix = '/' + str(wsPrefix)
    current_version = sparta_8c5bc8c8c4()
    try:
        b_call_update = False
        versioning_set = AppVersioning.objects.all()
        date_now = datetime.now().astimezone(UTC)
        if versioning_set.count() == 0:
            AppVersioning.objects.create(last_check_date=date_now)
            b_call_update = True
        else:
            versioning_obj = versioning_set[0]
            last_check_date = versioning_obj.last_check_date
            diff_date = date_now - last_check_date
            latest_version = versioning_obj.last_available_version_pip
            if not current_version == latest_version:
                b_call_update = True
            elif diff_date.seconds > 60 * 10:
                b_call_update = True
                versioning_obj.last_check_date = date_now
                versioning_obj.save()
    except:
        b_call_update = True
    try:
        api_path = sparta_bff35427ab()['api']
        with open(os.path.join(api_path, 'app_data_asgi.json'), 'r'
            ) as json_file:
            loaded_data_dict = json.load(json_file)
        ASGI_PORT = int(loaded_data_dict['default_port'])
    except:
        ASGI_PORT = 5664
    is_cypress_test = -1
    if os.environ.get('CYPRESS_TEST_APP', '0') == '1':
        is_cypress_test = 1
    hostWsPrefix = conf_settings.HOST_WS_PREFIX
    websocketPrefix = conf_settings.WEBSOCKET_PREFIX
    is_vite = conf_settings.IS_VITE
    if is_vite:
        if is_cypress_test == 1:
            is_vite = False
    context_var = {'PROJECT_NAME': conf_settings.PROJECT_NAME,
        'IS_DEV_VIEW_ENABLED': conf_settings.IS_DEV_VIEW_ENABLED,
        'CAPTCHA_SITEKEY': conf_settings.CAPTCHA_SITEKEY,
        'WEBSOCKET_PREFIX': websocketPrefix, 'URL_PREFIX': urlPrefix,
        'URL_WS_PREFIX': wsPrefix, 'ASGI_PORT': ASGI_PORT, 'HOST_WS_PREFIX':
        hostWsPrefix, 'CHECK_VERSIONING': b_call_update, 'CURRENT_VERSION':
        current_version, 'IS_VITE': is_vite, 'IS_DEV': conf_settings.IS_DEV,
        'IS_DOCKER': os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER', 'False') ==
        'True', 'CYPRESS_TEST_APP': is_cypress_test}
    return context_var


def sparta_6ae4813892(captcha) ->dict:
    """
    Validate Google Captcha
    """
    try:
        if captcha is not None:
            if len(captcha) > 0:
                CAPTCHA_SECRET_KEY = sparta_5f33e0d2c4()['CAPTCHA_SECRET_KEY']
                captcha_url = (
                    f'https://www.google.com/recaptcha/api/siteverify?secret={CAPTCHA_SECRET_KEY}&response={captcha}'
                    )
                res_req = requests.get(captcha_url)
                if int(res_req.status_code) == 200:
                    json_res = json.loads(res_req.text)
                    if json_res['success']:
                        return {'res': 1}
    except Exception as e:
        return {'res': -1, 'errorMsg': str(e)}
    return {'res': -1, 'errorMsg': 'Invalid captcha'}


def sparta_10f2573ca7(password) ->bool:
    """
    
    """
    userprofile_set = UserProfile.objects.filter(email=conf_settings.ADMIN_DEFAULT_EMAIL).all()
    if userprofile_set.count() == 0:
        return conf_settings.ADMIN_DEFAULT == password
    else:
        admin_user_obj = userprofile_set[0]
        user_obj = admin_user_obj.user
        return user_obj.check_password(password)


def sparta_23d9373307(code) ->bool:
    """
    Code to create a new account (env variable set when docker starts)
    """
    try:
        if code is not None:
            if len(code) > 0:
                spartaqube_password = os.getenv('SPARTAQUBE_PASSWORD', 'admin')
                if spartaqube_password == code:
                    return True
    except:
        return False
    return False


def sparta_9fb18a0f07(user) ->dict:
    """
    
    """
    dict_var = dict()
    if not user.is_anonymous:
        userprofile_set = UserProfile.objects.filter(user=user)
        if userprofile_set.count() > 0:
            userprofile_obj = userprofile_set[0]
            avatar_obj = userprofile_obj.avatar
            if avatar_obj is not None:
                avatar_obj = userprofile_obj.avatar.avatar
            dict_var['avatar'] = avatar_obj
            dict_var['userProfile'] = userprofile_obj
            editor_theme = userprofile_obj.editor_theme
            if editor_theme is None:
                editor_theme = 'default'
            elif len(editor_theme) == 0:
                editor_theme = 'default'
            else:
                editor_theme = userprofile_obj.editor_theme
            dict_var['theme'] = editor_theme
            dict_var['font_size'] = userprofile_obj.font_size
            dict_var['B_DARK_THEME'] = userprofile_obj.is_dark_theme
            dict_var['is_size_reduced_plot_db'
                ] = userprofile_obj.is_size_reduced_plot_db
            dict_var['is_size_reduced_api'
                ] = userprofile_obj.is_size_reduced_api
    dict_var['manifest'] = sparta_a193455a5d()
    return dict_var


def sparta_739eb337dc(user):
    """
    
    """
    dict_var = dict()
    dict_var['manifest'] = sparta_a193455a5d()
    return dict_var


def sparta_80ba3c80c9():
    try:
        socket.create_connection(('1.1.1.1', 53))
        return True
    except OSError:
        pass
    return False


def sparta_1907700568():
    """
    
    """
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    return hostname, IPAddr

#END OF QUBE
