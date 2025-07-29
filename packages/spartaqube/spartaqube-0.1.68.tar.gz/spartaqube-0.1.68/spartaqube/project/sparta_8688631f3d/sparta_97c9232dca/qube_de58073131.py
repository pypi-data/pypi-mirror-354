import os
import getpass
import json
import glob
from os import listdir
from os.path import isfile, join


def sparta_afa43143d0(json_data, userObj):
    """
    We manage two cases:
        1. Jupyter Directory (in order to load the jupyter server at a specific location). typeexplorer == 1
        2. Excel picker (in order to find and link and Excel file). typeexplorer != 1
    """
    typeexplorer = json_data['typeexplorer']
    if int(typeexplorer) == 1:
        jupyterDirectorySet = JupyterDirectory.objects.filter(user=userObj
            ).all()
        if jupyterDirectorySet.exists():
            jupyterDirectoryObj = jupyterDirectorySet[0]
            currentPath = jupyterDirectoryObj.directory
        else:
            currentPath = os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__))))
    else:
        username = getpass.getuser()
        currentPath = 'C:\\Users\\' + str(username) + '\\Desktop'
    try:
        folders, onlyfiles = sparta_07bf6146f7(currentPath,
            typeexplorer)
        res = {'res': 1, 'files': onlyfiles, 'folders': folders,
            'currentPath': currentPath}
    except:
        res = {'res': -1, 'msg': 'Path not found...'}
    return res


def sparta_278836d7b2(json_data, userObj):
    """
    Go one level up and returns files and folders
    """
    try:
        currentPath = json_data['currentPath']
        typeexplorer = json_data['typeexplorer']
        newPath = os.path.dirname(currentPath)
        folders, onlyfiles = sparta_07bf6146f7(newPath, typeexplorer)
        res = {'res': 1, 'files': onlyfiles, 'folders': folders,
            'currentPath': newPath}
    except:
        res = {'res': -1, 'msg': 'Path not found...'}
    return res


def sparta_138abef5ae(json_data, userObj):
    """
    Open folder and returns files and folders
    """
    try:
        currentPath = json_data['currentPath']
        typeexplorer = json_data['typeexplorer']
        folders, onlyfiles = sparta_07bf6146f7(currentPath,
            typeexplorer)
        res = {'res': 1, 'files': onlyfiles, 'folders': folders,
            'currentPath': currentPath}
    except:
        res = {'res': -1, 'msg': 'Path not found...'}
    return res


def sparta_07bf6146f7(currentPath, typeexplorer=None):
    onlyfiles = [f for f in listdir(currentPath) if isfile(join(currentPath,
        f))]
    if typeexplorer is not None:
        if int(typeexplorer) == 2:
            excelExtension = ['xls', 'xlsx', 'xlsm']
            onlyfiles = [thisObj for thisObj in onlyfiles if thisObj.split(
                '.')[-1] in excelExtension]
    folders = [o for o in os.listdir(currentPath) if os.path.isdir(os.path.join(currentPath, o))]
    return folders, onlyfiles


def sparta_56ccb9ea8a(currentPath):
    """
    Returns the structure of a directory recursively as a dictionary
    """

    def explore(starting_path):
        alld = {'': {}}
        for dirpath, dirnames, filenames in os.walk(starting_path):
            d = alld
            dirpathIni = dirpath
            dirpath = dirpath[len(starting_path):]
            for subd in dirpath.split(os.sep):
                based = d
                d = d[subd]
                if len(d) > 0:
                    d['___sq___path___'] = dirpathIni
                    d['___sq___show___'] = 0
            if dirnames:
                for dn in dirnames:
                    d[dn] = {}
            else:
                based[subd] = {'___sq___files___': filenames,
                    '___sq___path___': dirpathIni, '___sq___show___': 0}
        return alld['']
    res_dict = explore(currentPath)

    def addBaseFiles(tmp_dict, tmp_path):
        tmp_dict['___sq___files___'] = [f for f in listdir(tmp_path) if
            isfile(join(tmp_path, f))]
        tmp_dict['___sq___path___'] = tmp_path
        for k, v in tmp_dict.items():
            if isinstance(v, dict):
                addBaseFiles(v, os.path.join(tmp_path, k))
    if isinstance(res_dict, dict):
        addBaseFiles(res_dict, currentPath)
        res_dict['___sq___files___'] = [f for f in listdir(currentPath) if
            isfile(join(currentPath, f))]
        res_dict['___sq___path___'] = currentPath
        res_dict['___sq___show___'] = 1
    else:
        res_dict = {'___sq___files___': res_dict, '___sq___path___':
            currentPath, '___sq___show___': 1}
    return res_dict

#END OF QUBE
