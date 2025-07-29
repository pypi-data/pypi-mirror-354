import os
import json
import asyncio
import subprocess
import platform
from pathlib import Path
from channels.generic.websocket import AsyncWebsocketConsumer
from spartaqube_app.path_mapper_obf import sparta_bff35427ab
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de
from project.logger_config import logger


class HotReloadLivePreviewWS(AsyncWebsocketConsumer):
    """
    WebSocket consumer for hot reload and live preview
    Whenever a change is detected, we build the dist main.js using esbuild
    """

    async def connect(self):
        """
        Handle WebSocket connection
        """
        logger.debug('Connect Now')
        self.isSocketKilled = False
        self.monitor_task = None
        self.user = self.scope['user']
        await self.accept()

    async def disconnect(self, close_code=None):
        """
        Handle WebSocket disconnection
        """
        logger.debug('Disconnect')
        self.isSocketKilled = True
        try:
            await self.close()
        except:
            pass
        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                logger.debug('Monitoring task cancelled.')

    def build_dist(self) ->dict:
        """
        Build the web application and returns dictionary, especially the error message if an ivnalid syntax is present in the codebase
        """
        system = platform.system()
        arch = platform.machine()
        core_developer_path = sparta_bff35427ab()['project/core/developer']
        esbuild_path = os.path.join(core_developer_path, 'esbuild')
        if system == 'Linux' and arch in ['x86_64']:
            esbuild_binary = 'esbuild-linux-x64'
        elif system == 'Darwin' and arch in ['x86_64']:
            esbuild_binary = 'esbuild-darwin-x64'
        elif system == 'Darwin' and arch in ['arm64']:
            esbuild_binary = 'esbuild-darwin-arm64'
        elif system in ['Windows'] and arch in ['AMD64']:
            esbuild_binary = 'esbuild-windows-x64.exe'
        else:
            raise RuntimeError(f'Unsupported platform: {system} {arch}')
        esbuild_binary = os.path.join(esbuild_path, esbuild_binary)
        input_js = os.path.join(self.project_path, 'frontend', 'main.js')
        output_js = os.path.join(self.project_path, 'frontend', 'dist',
            'main.js')
        try:
            result = subprocess.run([esbuild_binary, input_js, '--bundle',
                '--minify', f'--outfile={output_js}'], check=True, stdout=
                subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                encoding='utf-8')
            logger.debug('Build successful:')
            logger.debug(result.stdout)
            return {'res': 1, 'stdout': result.stdout}
        except Exception as e:
            logger.debug('Error occurred:')
            logger.debug(e)
            error_msg = str(e)
            return {'res': -1, 'stderr': error_msg}

    async def monitor_folder(self, path_to_watch, excluded_subfolders: list):
        """
        Monitor the specified folder for changes, excluding specified subfolders
        """
        file_mod_times = dict()
        while not self.isSocketKilled:
            try:
                changes_detected = False
                current_files = []
                for root, dirs, files in os.walk(path_to_watch):
                    normalized_root = sparta_226d9606de(root)
                    if any(normalized_root.startswith(subfolder) for
                        subfolder in excluded_subfolders):
                        continue
                    for file_name in files:
                        if file_name.split('.')[-1] == 'pyc':
                            continue
                        file_path = os.path.join(root, file_name)
                        current_files.append(file_path)
                        last_mod_time = os.stat(file_path).st_mtime
                        if file_path not in file_mod_times or file_mod_times[
                            file_path] != last_mod_time:
                            file_mod_times[file_path] = last_mod_time
                            changes_detected = True
                            logger.debug(
                                f'Changes hot reload1 due to {file_name} where root {root}'
                                )
                monitored_files = list(file_mod_times.keys())
                for monitored_file in monitored_files:
                    if monitored_file not in current_files:
                        del file_mod_times[monitored_file]
                        changes_detected = True
                        logger.debug(
                            f'Changes hot reload2 due to {monitored_file}')
                if changes_detected:
                    res_build_dict = self.build_dist()
                    if res_build_dict['res'] == 1:
                        res = {'res': 1, 'triggerChanges': 1}
                    else:
                        res = {'res': -1, 'stderr': res_build_dict['stderr']}
                    res_json = json.dumps(res)
                    await self.send(text_data=res_json)
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                logger.debug('Monitoring task cancelled.')
                break
            except Exception as e:
                logger.debug(f'Error monitoring folder: {e}')
                break

    async def receive(self, text_data):
        """
        Handle incoming WebSocket messages
        """
        if len(text_data) > 0:
            json_data = json.loads(text_data)
            project_path = sparta_226d9606de(json_data['projectPath'])
            self.project_path = project_path
            excluded_folders = [os.path.join(project_path, 'backend/logs'),
                os.path.join(project_path, 'frontend/dist')]
            excluded_folders = [sparta_226d9606de(elem) for elem in
                excluded_folders]
            if self.monitor_task and not self.monitor_task.done():
                self.monitor_task.cancel()
                try:
                    await self.monitor_task
                except asyncio.CancelledError:
                    logger.debug('Previous monitoring task cancelled.')
            self.monitor_task = asyncio.create_task(self.monitor_folder(
                project_path, excluded_folders))

#END OF QUBE
