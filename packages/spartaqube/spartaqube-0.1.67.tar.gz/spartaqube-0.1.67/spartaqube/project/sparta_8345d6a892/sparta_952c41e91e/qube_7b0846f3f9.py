import os
import subprocess
import platform
from project.sparta_8345d6a892.sparta_952c41e91e.qube_41685030f2 import sparta_ad557db230, sparta_91bd932e94


def sparta_e6a027bd1e(folder_path) ->dict:
    """
    Open a folder in VSCode.Args:
        folder_path (str): Path to the folder to open in VSCode.Raises:
        FileNotFoundError: If the folder does not exist.EnvironmentError: If VSCode is not installed."""
    folder_path = sparta_ad557db230(folder_path)
    if not os.path.isdir(folder_path):
        return {'res': -1, 'errorMsg':
            f"The folder path '{folder_path}' does not exist."}
    system_platform = platform.system()
    try:
        if system_platform == 'Windows':
            command = f'start cmd /c code "{folder_path}"'
            os.system(command)
        elif system_platform == 'Darwin':
            command = (
                f'osascript -e \'tell application "Terminal" to do script "code \\"{folder_path}\\" && exit"\''
                )
            subprocess.run(command, shell=True)
        elif system_platform == 'Linux':
            command = (
                f'gnome-terminal -- bash -c \'code "{folder_path}"; exit\'')
            subprocess.run(command, shell=True)
        else:
            return {'res': -1, 'errorMsg':
                f'Unsupported platform: {system_platform}'}
    except Exception as e:
        return {'res': -1, 'errorMsg': f'Failed to open folder in VSCode: {e}'}
    return {'res': 1}


def sparta_7d51b73540(folder_path) ->dict:
    """
    Open terminal
    """
    path = sparta_ad557db230(folder_path)
    if not os.path.isdir(path):
        return {'res': -1, 'errorMsg':
            f"The provided path '{path}' is not a valid directory."}
    system = platform.system()
    try:
        if system == 'Windows':
            os.system(f'start cmd /K "cd /d {path}"')
        elif system == 'Linux':
            subprocess.run(['x-terminal-emulator', '--working-directory',
                path], check=True)
        elif system == 'Darwin':
            script = f"""
            tell application "Terminal"
                do script "cd {path}"
                activate
            end tell
            """
            subprocess.run(['osascript', '-e', script], check=True)
        else:
            return {'res': -1, 'errorMsg': 'Unsupported operating system.'}
    except Exception as e:
        return {'res': -1, 'errorMsg':
            f"Failed to open terminal at '{path}': {e}"}
    return {'res': 1}

#END OF QUBE
