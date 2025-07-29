import os, sys
import shutil
import datetime
import simplejson as json
from pathlib import Path
from datetime import datetime
from spartaqube_app.path_mapper_obf import sparta_b6a401eb72
from project.logger_config import logger
main_api = sparta_b6a401eb72()['api']
sys.path.insert(0, main_api)
from spartaqube_utils import is_scalar, safe_to_json, rename_duplicate_columns, convert_dataframe_to_json, convert_to_dataframe, convert_to_dataframe_func, process_dataframe_components


def sparta_91bd932e94(path):
    with open(path, 'a'):
        os.utime(path, None)


def sparta_ad557db230(path):
    """
    This method returns the absolute, normalized version of the path. It resolves symlinks as well, if present
    """
    normalized_path = Path(path).resolve()
    return str(normalized_path)


def sparta_d6ce78db3e(textOutputArr):
    """

    """
    resPrintArr = textOutputArr
    try:
        resPrintArr = [thisObj for thisObj in resPrintArr if len(thisObj) > 0]
        resPrintArr = [thisObj for thisObj in resPrintArr if thisObj !=
            'Welcome to SpartaQube API']
        resPrintArr = [thisObj for thisObj in resPrintArr if thisObj !=
            "<span style='color:#0ab70a'>You are logged</span>"]
        resPrintArr = [thisObj for thisObj in resPrintArr if thisObj !=
            'You are logged']
    except Exception as e:
        pass
    return resPrintArr


def sparta_e647fdde7b(input2JsonEncode, dateFormat=None):
    """
        Encoder for numpy variables
        dateFormat = '%Y-%m-%d %H:%M:%S' if we need to encode datetime variables
    """
    import numpy as np


    class NpEncoder(json.JSONEncoder):

        def default(self, obj):
            if isinstance(obj, np.integer):
                return int(obj)
            if isinstance(obj, np.floating):
                return float(obj)
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, datetime.datetime):
                if dateFormat is not None:
                    return obj.strftime(dateFormat)
                else:
                    return str(obj)
            return super(NpEncoder, self).default(obj)
    resJson = json.dumps(input2JsonEncode, ignore_nan=True, cls=NpEncoder)
    return resJson


def sparta_2abbcd21bc(path):
    """
    
    """
    try:
        os.rmdir(path)
    except:
        try:
            os.system('rmdir /S /Q "{}"'.format(path))
        except:
            try:
                shutil.rmtree(path)
            except:
                try:
                    os.remove(path)
                except:
                    pass


def sparta_7bd6291cd8(file_path):
    """
    
    """
    try:
        os.remove(file_path)
        logger.debug(f"File '{file_path}' has been deleted.")
    except Exception as e:
        try:
            os.unlink(file_path)
            logger.debug(f"File '{file_path}' has been forcefully deleted.")
        except Exception as e:
            logger.debug(f'An error occurred while deleting the file: {e}')

#END OF QUBE
