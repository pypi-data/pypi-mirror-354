import os, platform, getpass


def sparta_f9f684c510() ->bool:
    """
    Test if we are on the docker platform
    """
    try:
        is_docker_platform = str(os.environ.get(
            'IS_REMOTE_SPARTAQUBE_CONTAINER', 'False')) == 'True'
    except:
        is_docker_platform = False
    return is_docker_platform


def sparta_934007d073() ->str:
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'mac'
    else:
        return None


def sparta_9c89cfd808() ->str:
    """
    SpartaQube volume path is the path where we store the resources like (ipynb): notebook, dashboard, kernel, developer apps etc..."""
    if sparta_f9f684c510():
        return '/spartaqube'
    platform = sparta_934007d073()
    if platform == 'windows':
        default_project_path = f'C:\\Users\\{getpass.getuser()}\\SpartaQube'
    elif platform == 'linux':
        default_project_path = os.path.expanduser('~/SpartaQube')
    elif platform == 'mac':
        default_project_path = os.path.expanduser(
            '~/Library/Application Support\\SpartaQube')
    return default_project_path

#END OF QUBE
