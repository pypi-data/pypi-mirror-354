import os, sys
import json
import ast
import re
import base64
import uuid
import hashlib
import socket
import cloudpickle
import websocket
import subprocess, threading
from random import randint
import pandas as pd
from pathlib import Path
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings as conf_settings
import pytz
UTC = pytz.utc
from project.models import UserProfile


def sparta_2bb8a248b0(json_data, user_obj) ->dict:
    """
    Save param user reduce size plotDB
    """
    is_size_reduced = json_data['is_size_reduced']
    user_profile_set = UserProfile.objects.filter(user=user_obj)
    if user_profile_set.count() > 0:
        user_profile_obj = user_profile_set[0]
        user_profile_obj.is_size_reduced_plot_db = is_size_reduced
        user_profile_obj.save()
    return {'res': 1}


def sparta_c9ca6c556b(json_data, user_obj) ->dict:
    """
    Save param user reduce size plotDB
    """
    is_size_reduced = json_data['is_size_reduced']
    user_profile_set = UserProfile.objects.filter(user=user_obj)
    if user_profile_set.count() > 0:
        user_profile_obj = user_profile_set[0]
        user_profile_obj.is_size_reduced_api = is_size_reduced
        user_profile_obj.save()
    return {'res': 1}

#END OF QUBE
