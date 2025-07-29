import json
import base64
import hashlib, re, uuid
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
import pytz
UTC = pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import User, UserProfile
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054


def sparta_777638e1f2(is_owner=False) ->dict:
    return {'is_owner': is_owner, 'is_admin': True, 'has_write_rights': 
        True, 'has_reshare_rights': True}


def sparta_cb015f1a63() ->dict:
    return {'is_owner': False, 'is_admin': False, 'has_write_rights': False,
        'has_reshare_rights': False}


def sparta_5c6007e1fe(user_obj, portfolio_obj):
    """
    
    """
    if portfolio_obj.user == user_obj:
        return sparta_777638e1f2(True)
    userGroupUserSet = qube_1d2a59f054.sparta_1c22139619(user_obj)
    userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
    if len(userGroups) > 0:
        portfolio_shared_set = PortfolioShared.objects.filter(Q(is_delete=0,
            userGroup__in=userGroups, portfolio=portfolio_obj) & ~Q(
            portfolio__user=user_obj) | Q(is_delete=0, user=user_obj,
            portfolio=portfolio_obj))
    else:
        portfolio_shared_set = PortfolioShared.objects.filter(is_delete=0,
            user=user_obj, portfolio=portfolio_obj)
    if portfolio_shared_set.count() == 0:
        return sparta_cb015f1a63()
    portfolio_shared_obj = portfolio_shared_set[0]
    share_rights_obj = portfolio_shared_obj.ShareRights
    if share_rights_obj.is_delete:
        return sparta_cb015f1a63()
    return {'is_owner': False, 'is_admin': share_rights_obj.is_admin,
        'has_write_rights': share_rights_obj.has_write_rights,
        'has_reshare_rights': share_rights_obj.has_reshare_rights}


def sparta_8bf58b835b(user_obj, universe_obj):
    """
    
    """
    if universe_obj.user == user_obj:
        return sparta_777638e1f2()
    userGroupUserSet = qube_1d2a59f054.sparta_1c22139619(user_obj)
    userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
    if len(userGroups) > 0:
        universe_shared_set = UniverseShared.objects.filter(Q(is_delete=0,
            userGroup__in=userGroups, universe=universe_obj) & ~Q(
            universe__user=user_obj) | Q(is_delete=0, user=user_obj,
            universe=universe_obj))
    else:
        universe_shared_set = UniverseShared.objects.filter(is_delete=0,
            user=user_obj, universe=universe_obj)
    if universe_shared_set.count() == 0:
        return sparta_cb015f1a63()
    universe_shared_obj = universe_shared_set[0]
    share_rights_obj = universe_shared_obj.ShareRights
    if share_rights_obj.is_delete:
        return sparta_cb015f1a63()
    return {'is_admin': share_rights_obj.is_admin, 'has_write_rights':
        share_rights_obj.has_write_rights, 'has_reshare_rights':
        share_rights_obj.has_reshare_rights}

#END OF QUBE
