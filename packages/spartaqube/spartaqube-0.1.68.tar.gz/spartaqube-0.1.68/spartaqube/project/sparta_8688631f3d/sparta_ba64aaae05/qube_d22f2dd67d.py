import re
import os
import json
import stat
import importlib
import io, sys
import subprocess
import platform
import base64
import traceback
import uuid
import shutil
from pathlib import Path
from django.db.models import Q
from django.utils.text import slugify
from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.models import ShareRights
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_5d2f5154f8 import qube_c71ace27e3 as qube_c71ace27e3
from project.sparta_8688631f3d.sparta_577b784581.qube_2949549c51 import Connector as Connector
from project.sparta_8688631f3d.sparta_97c9232dca import qube_de58073131 as qube_de58073131
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_4009e9a33a as qube_4009e9a33a
from project.sparta_8688631f3d.sparta_9df5aeb023 import qube_49f539b4d6 as qube_49f539b4d6
from project.sparta_8688631f3d.sparta_5149e63dd6.qube_0a8e8bbdab import sparta_8c5bc8c8c4
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_cdd2396883 import sparta_99859b53bb, sparta_f8e322f1b3
from project.logger_config import logger
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_f0d228f17a import sparta_ca71f9cc05
from project.sparta_8688631f3d.sparta_68bfd7a828 import qube_d1459513cb as qube_d1459513cb


def sparta_09abdd9532(user_obj) ->list:
    """
    
    """
    user_group_set = qube_1d2a59f054.sparta_1c22139619(user_obj)
    if len(user_group_set) > 0:
        user_groups = [this_obj.user_group for this_obj in user_group_set]
    else:
        user_groups = []
    return user_groups


def sparta_2a3abc3781(json_data, user_obj) ->dict:
    """
    Load developer library: all my developer view + the public (exposed) views
    """
    json_data['is_plot_db'] = True
    return qube_d1459513cb.sparta_b0f7dbf938(json_data, user_obj)


def sparta_fc599b1f6c() ->str:
    """
    Get default plotDB developer project path
    """
    spartaqube_volume_path = sparta_ca71f9cc05()
    default_plot_db_project_path = os.path.join(spartaqube_volume_path,
        'plot_db_developer')

    def create_folder_if_not_exists(path):
        folder_path = Path(path)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)
    create_folder_if_not_exists(default_plot_db_project_path)
    return {'res': 1, 'path': default_plot_db_project_path}

#END OF QUBE
