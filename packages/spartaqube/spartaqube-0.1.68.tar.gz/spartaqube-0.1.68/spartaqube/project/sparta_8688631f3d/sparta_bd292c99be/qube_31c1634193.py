import os, sys
import platform
import subprocess
if platform.system() == 'Windows':
    import pythoncom
    import win32com.client
from pathlib import Path
from project.sparta_8688631f3d.sparta_34d32fb8c6 import qube_cbe6ad2077 as qube_cbe6ad2077
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.logger_config import logger
from django.conf import settings as conf_settings


def sparta_226d9606de(path):
    """
    This method returns the absolute, normalized version of the path. It resolves symlinks as well, if present
    """
    normalized = Path(path).resolve()
    return str(normalized).replace('\\', '\\\\')


def sparta_4c280660d0():
    is_virtual_env = hasattr(sys, 'real_prefix') or hasattr(sys, 'base_prefix'
        ) and sys.base_prefix != sys.prefix
    if is_virtual_env:
        virtual_env_path = sys.prefix
        virtual_env_name = os.path.basename(virtual_env_path)
        return {'is_virtual_env': True, 'virtual_env_name':
            virtual_env_name, 'virtual_env_path': sparta_226d9606de(
            virtual_env_path)}
    else:
        return {'is_virtual_env': False, 'virtual_env_name': None,
            'virtual_env_path': None}


def sparta_f808c7fcf2(bat_file_path, shortcut_path, icon_path):
    """
    Create a .lnk shortcut for a .bat file with a custom icon.Args:
        bat_file_path (str): Path to the .bat file.shortcut_path (str): Path to save the .lnk shortcut file.icon_path (str): Path to the icon file (.ico) to use for the shortcut.Returns:
        None
    """
    pythoncom.CoInitialize()
    try:
        bat_file_path = os.path.abspath(bat_file_path)
        shortcut_path = os.path.abspath(shortcut_path)
        icon_path = os.path.abspath(icon_path)
        shell = win32com.client.Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = bat_file_path
        shortcut.WorkingDirectory = os.path.dirname(bat_file_path)
        shortcut.IconLocation = icon_path
        shortcut.Save()
        logger.debug('icon_path')
        logger.debug(icon_path)
        logger.debug(f'Shortcut created at: {shortcut_path}')
    finally:
        pythoncom.CoUninitialize()


def sparta_b2ed0c71fe(shell_script_path, shortcut_name, icon_path):
    """
    Create a macOS shortcut (.app) for a shell script that appears in Launchpad.Args:
        shell_script_path (str): Path to the shell script (e.g., SpartaQube.sh).shortcut_name (str): Name of the shortcut (e.g., "SpartaQube Launcher").icon_path (str): Path to the icon file (.icns format).Returns:
        None
    """
    shell_script_path = os.path.abspath(shell_script_path)
    icon_path = os.path.abspath(icon_path)
    app_dir = f'/Applications/{shortcut_name}.app'
    os.makedirs(f'{app_dir}/Contents/MacOS', exist_ok=True)
    os.makedirs(f'{app_dir}/Contents/Resources', exist_ok=True)
    exec_script_path = f'{app_dir}/Contents/MacOS/{shortcut_name}'
    with open(exec_script_path, 'w') as exec_script:
        exec_script.write(
            f"""#!/bin/bash
osascript -e 'tell application "Terminal"
    do script "bash {shell_script_path}"
end tell'
"""
            )
    os.chmod(exec_script_path, 493)
    plist_content = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>CFBundleExecutable</key>
        <string>{shortcut_name}</string>
        <key>CFBundleIconFile</key>
        <string>{os.path.basename(icon_path)}</string>
        <key>CFBundleName</key>
        <string>{shortcut_name}</string>
        <key>CFBundleIdentifier</key>
        <string>com.example.{shortcut_name.lower()}</string>
        <key>CFBundleVersion</key>
        <string>1.0</string>
        <key>CFBundlePackageType</key>
        <string>APPL</string>
    </dict>
    </plist>
    """
    plist_path = f'{app_dir}/Contents/Info.plist'
    with open(plist_path, 'w') as plist_file:
        plist_file.write(plist_content.strip())
    resources_icon_path = (
        f'{app_dir}/Contents/Resources/{os.path.basename(icon_path)}')
    if os.path.exists(icon_path):
        subprocess.run(['cp', icon_path, resources_icon_path])
    else:
        logger.debug(f'Icon file not found: {icon_path}')
    subprocess.run(['killall', 'Dock'])
    logger.debug(f'Shortcut created at: {app_dir}')
    logger.debug(
        f'Logs will be written to /tmp/{shortcut_name.lower()}_log.txt')


def sparta_3bf76d64a8(shortcut_name, shell_script_path, icon_path):
    """
    Create a Linux desktop launcher that executes a shell script.Args:
        shortcut_name (str): Name of the desktop shortcut (e.g., "SpartaQube").shell_script_path (str): Absolute path to the shell script to execute.icon_path (str): Absolute path to the .png or .svg icon file.Returns:
        None
    """
    shell_script_path = os.path.abspath(shell_script_path)
    icon_path = os.path.abspath(icon_path)
    desktop_file_path = os.path.expanduser(f'~/Desktop/{shortcut_name}.desktop'
        )
    desktop_content = f"""[Desktop Entry]
Type=Application
Name={shortcut_name}
Exec=gnome-terminal -- bash -c "bash {shell_script_path}; exec bash"
Icon={icon_path}
Terminal=true
"""
    with open(desktop_file_path, 'w') as desktop_file:
        desktop_file.write(desktop_content)
    os.chmod(desktop_file_path, 493)
    logger.debug(f'Launcher created at: {desktop_file_path}')
    logger.debug(
        f'Double-click the icon on your desktop to launch {shortcut_name}.')


def sparta_45a8d0da27(json_data, user_obj) ->dict:
    """
    Create desktop launcher
    """
    api_token_dict = qube_cbe6ad2077.sparta_f468ac685f(json_data, user_obj)
    if api_token_dict['res'] == 1:
        token = api_token_dict['token']
        api_path = sparta_bff35427ab()['api']
        spartaqube_exec = sparta_226d9606de(os.path.join(api_path,
            'spartaqube_exec.py'))
        if os.path.exists(spartaqube_exec):
            try:
                os.remove(spartaqube_exec)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
        code_executable = f"""
from spartaqube import Spartaqube as Spartaqube

if __name__ == '__main__':
    Spartaqube(api_key='{token}', b_open_browser=True)

"""
        with open(spartaqube_exec, 'w') as file:
            file.write(code_executable)
        spartaqube_launcher = sparta_226d9606de(os.path.join(api_path,
            'spartaqube_launcher.py'))
        if os.path.exists(spartaqube_launcher):
            try:
                os.remove(spartaqube_launcher)
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
        env_info = sparta_4c280660d0()
        logger.debug('env_info')
        logger.debug(env_info)
        if env_info['is_virtual_env']:
            venv_path = env_info['virtual_env_path']
            python_executable = sparta_226d9606de(os.path.join(f'{venv_path}',
                'bin', 'python') if os.name != 'nt' else os.path.join(
                f'{venv_path}', 'Scripts', 'python.exe'))
            activation_script = sparta_226d9606de(os.path.join(f'{venv_path}',
                'bin/activate') if os.name != 'nt' else os.path.join(
                venv_path, 'Scripts/activate.bat'))
            code_launcher_icon = f"""
import os
import sys
import subprocess
import platform

def main_launcher():
    is_windows = platform.system() == "Windows"
    if not os.path.exists('{venv_path}'):
        print(f"Virtual environment not found")
        sys.exit(1)

    if not os.path.exists('{python_executable}'):
        raise FileNotFoundError(f"Python executable not found")
    if not os.path.exists('{spartaqube_exec}'):
        raise FileNotFoundError(f"Script not found")

    if is_windows:
        # On Windows: Activate the virtual environment using cmd.exe
        command = f'cmd.exe /k "{activation_script} && python "{spartaqube_exec}"'
        subprocess.run(command, shell=True)
    else:
        # On macOS/Linux: Use bash to activate the virtual environment
        command = f'source "{activation_script}" && python "{spartaqube_exec}"'
        subprocess.run(command, shell=True, executable="/bin/bash")

if __name__ == "__main__":
    main_launcher()
"""
        else:
            code_launcher_icon = f"""
import os
import sys
import subprocess

def main_launcher():
    # Path to the Python executable in the file system
    python_executable = sys.executable

    if not os.path.exists(python_executable):
        print(f"Python executable not found in virtual environment")
        sys.exit(1)

    # Path to your application
    script_path = "{spartaqube_exec}"

    if not os.path.exists(script_path):
        print(f"Application script not found: {spartaqube_exec}")
        sys.exit(1)

    # Run the Python application
    subprocess.run([python_executable, script_path])

if __name__ == "__main__":
    main_launcher()
"""
        logger.debug('spartaqube_launcher')
        logger.debug(spartaqube_launcher)
        with open(spartaqube_launcher, 'w') as file:
            file.write(code_launcher_icon)
        spartaqube_path = sparta_bff35427ab()['spartaqube_path']
        if conf_settings.IS_DEV:
            icon_path = sparta_226d9606de(os.path.join(spartaqube_path,
                'static', 'assets', 'images', 'Icon', 'favicon512.ico'))
        else:
            icon_path = sparta_226d9606de(os.path.join(spartaqube_path,
                'staticfiles', 'assets', 'images', 'Icon', 'favicon512.ico'))
        platform_system = platform.system()
        if platform_system == 'Windows':
            spartaqube_platform = sparta_226d9606de(os.path.join(api_path,
                'SpartaQube.bat'))
            spartaqube_lnk = sparta_226d9606de(os.path.join(api_path,
                'SpartaQube.lnk'))
            if os.path.exists(spartaqube_lnk):
                try:
                    os.remove(spartaqube_lnk)
                except Exception as e:
                    return {'res': -1, 'errorMsg': str(e)}
            sparta_f808c7fcf2(spartaqube_platform, spartaqube_lnk, icon_path)
            desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
            shortcut_path = os.path.join(desktop_path, 'SpartaQube.lnk')
            sparta_f808c7fcf2(spartaqube_platform, shortcut_path, icon_path)
        elif platform_system == 'Darwin':
            spartaqube_platform = sparta_226d9606de(os.path.join(api_path,
                'SpartaQube.sh'))
            sparta_b2ed0c71fe(shell_script_path=
                spartaqube_platform, shortcut_name='SpartaQube Launcher',
                icon_path=icon_path)
        else:
            spartaqube_platform = sparta_226d9606de(os.path.join(api_path,
                'SpartaQube.sh'))
            sparta_3bf76d64a8(shell_script_path=spartaqube_platform,
                shortcut_name='SpartaQube Launcher', icon_path=
                '/path/to/your/icon.png')
    return {'res': 1}

#END OF QUBE
