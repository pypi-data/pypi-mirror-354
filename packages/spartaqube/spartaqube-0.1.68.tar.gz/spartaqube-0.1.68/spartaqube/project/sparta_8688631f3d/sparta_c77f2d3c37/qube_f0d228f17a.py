import os, platform, getpass


def sparta_514b10b7c2() ->bool:
    """
    Test if we are on the docker platform
    """
    try:
        is_docker_platform = str(os.environ.get(
            'IS_REMOTE_SPARTAQUBE_CONTAINER', 'False')) == 'True'
    except:
        is_docker_platform = False
    return is_docker_platform


def sparta_af7fb9ae39() ->str:
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Linux':
        return 'linux'
    elif system == 'Darwin':
        return 'mac'
    else:
        return None


def sparta_ca71f9cc05() ->str:
    """
    SpartaQube volume path is the path where we store the resources like (ipynb): notebook, dashboard, kernel, developer apps etc..."""
    if sparta_514b10b7c2():
        return '/spartaqube'
    platform = sparta_af7fb9ae39()
    if platform == 'windows':
        default_project_path = f'C:\\Users\\{getpass.getuser()}\\SpartaQube'
    elif platform == 'linux':
        default_project_path = os.path.expanduser('~/SpartaQube')
    elif platform == 'mac':
        default_project_path = os.path.expanduser(
            '~/Library/Application Support\\SpartaQube')
    return default_project_path

#END OF QUBE
