import os, re, time, json, shutil
import git
from asyncio import subprocess
from re import S
from dateutil import parser
from subprocess import Popen, PIPE
from django.contrib.humanize.templatetags.humanize import naturalday
from project.logger_config import logger


def sparta_15237d9e1c(path) ->bool:
    """
    This function test if the path was git init
    """
    try:
        _ = git.Repo(path).git_dir
        return True
    except git.exc.InvalidGitRepositoryError:
        return False


def sparta_e2b0d1c1a2(json_data, user_obj):
    notebookProjectId = json_data['notebookProjectId']
    sqNotebookProjectSharedObj, _ = qube_9fb9ed74d5.get_notebookProjectObj(
        notebookProjectId, user_obj)
    if sqNotebookProjectSharedObj is not None:
        return True
    return False


def sparta_92e2d833fe(remoteBranchToTrack):
    """
    
    """
    proc = Popen(f'git branch -u {remoteBranchToTrack}', stdout=PIPE,
        stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, shell
        =True)
    realtime_output = proc.stdout.readline()
    logger.debug('realtime_output 1')
    logger.debug(realtime_output)
    proc = Popen(f'git config push.default upstream', stdout=PIPE, stderr=
        subprocess.STDOUT, bufsize=1, universal_newlines=True, shell=True)
    logger.debug('realtime_output 2')
    logger.debug(realtime_output)


def sparta_73d5f22424(func):
    """
        Decorator to check if the notebook is already created
    """

    def wrapper(json_data, user_obj):
        if not sparta_e2b0d1c1a2(json_data, user_obj):
            return {'res': -1, 'errorMsg':
                'You need to create a notebook first (you can save this notebook with CTRL+ALT+S first)'
                }
        return func(json_data, user_obj)
    return wrapper


def sparta_5868d0a6d9(func):
    """
        Decorator to check if the notebook is already created
    """

    def wrapper(webSocket, json_data, user_obj):
        if not sparta_e2b0d1c1a2(json_data, user_obj):
            return {'res': -1, 'errorMsg':
                'You need to create a notebook first (you can save this notebook with CTRL+ALT+S first)'
                }
        return func(webSocket, json_data, user_obj)
    return wrapper


def sparta_e3a30d0668(repo, user_obj):
    """
    
    """
    git_email = user_obj.email
    username = (
        f'{user_obj.first_name.capitalize()} {user_obj.last_name.capitalize()}'
        )
    with repo.config_writer() as config:
        config.set_value('user', 'name', username)
        config.set_value('user', 'email', git_email)


def sparta_2d7c3c78db(webSocket, json_data, user_obj):
    """
    Clone a repo in a folder
    """
    logger.debug('sqEditorGitClone')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    bCreateRepoAtPath = json_data['bCreateRepoAtPath']
    folder_name = json_data['folder_name']
    file_path = json_data['file_path']
    cloneUrl = json_data['cloneUrl']
    path_repo_clone = project_path
    if bCreateRepoAtPath:
        path_repo_clone = file_path
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path_repo_clone)
    proc = Popen(f'git clone {cloneUrl} --progress', stdout=PIPE, stderr=
        subprocess.STDOUT, bufsize=1, universal_newlines=True, shell=True)
    os.chdir(dir_path)
    bSuccess = False
    while True:
        realtime_output = proc.stdout.readline()
        if 'Receiving objects:' in realtime_output:
            bSuccess = True,
        if realtime_output == '' and proc.poll() is not None:
            break
        if realtime_output:
            webSocket.send(text_data=json.dumps({'res': 2, 'msg':
                realtime_output}))
    if bSuccess:
        return {'res': 1}
    else:
        return {'res': -1, 'errorMsg': 'An error occurred'}


def sparta_95f2a59d86(json_data, user_obj):
    """
    Create a new local repository
    """
    project_path = json_data['projectPath']
    b_add_gitignore = json_data.get('bAddGitignore', False)
    b_add_readme = json_data.get('bAddReadme', False)
    proc = Popen(f'git init', stdout=PIPE, stderr=subprocess.STDOUT,
        bufsize=1, universal_newlines=True, shell=True, cwd=project_path)
    output_lines = []
    for line in proc.stdout:
        logger.debug('Git create repo txt')
        logger.debug(line, end='')
        output_lines.append(line.strip())
    proc.stdout.close()
    proc.wait()
    current_path = os.path.dirname(__file__)
    if b_add_gitignore:
        source_file = os.path.join(current_path, '.default_gitignore')
        target_file = os.path.join(project_path, '.gitignore')
        try:
            shutil.copy(source_file, target_file)
        except:
            pass
    if b_add_readme:
        source_file = os.path.join(current_path, '.default_readme')
        target_file = os.path.join(project_path, 'README.md')
        try:
            shutil.copy(source_file, target_file)
        except:
            pass
    return {'res': 1, 'output': '\n'.join(output_lines)}


def sparta_c07cee739f(json_data, user_obj):
    """
    Add remote origin
    """
    logger.debug('sqEditorGitAddRemoteOrigin json_data')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        remote_url = json_data['remoteUrl']
        remote_name = json_data['remoteName']
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        remote = repo.create_remote(remote_name, url=remote_url)
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        for this_remote in repo.remotes:
            this_remote.fetch()
        for this_remote in repo.remotes:
            if remote == this_remote:
                refs_arr = this_remote.refs
                if len(refs_arr) > 0:
                    this_branch = refs_arr[len(refs_arr) - 1]
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    os.chdir(project_path)
                    sparta_92e2d833fe(this_branch)
                    os.chdir(dir_path)
    return {'res': 1}


def sparta_8dcb2da4ea(json_data, user_obj):
    """
    Load available remote branches to track
    """
    logger.debug('git_load_available_track_remote json_data')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        scm = json_data['scm']
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        available_branches = []
        for this_remote in repo.remotes:
            if scm == this_remote.config_reader.get('url'):
                for this_ref in this_remote.refs:
                    available_branches.append({'name': this_ref.name})
    return {'res': 1, 'available_branches': available_branches}


def sparta_8eeea64f46(json_data, user_obj):
    """
    Set track remote
    """
    logger.debug('*******************************************')
    logger.debug('git_set_track_remote json_data')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        scm = json_data['scm']
        remoteBranchToTrack = json_data['remoteBranchToTrack']
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        current_branch = repo.head.ref.name
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(project_path)
        sparta_92e2d833fe(remoteBranchToTrack)
        os.chdir(dir_path)
    return {'res': 1}


@sparta_73d5f22424
def sparta_cfacadb7dc(json_data, user_obj):
    """
    Update repo settings
    """
    return {'res': 1}


def sparta_61a32ef1ad(json_data, user_obj):
    """
    Pull repo
    """
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        branch = repo.active_branch
        remote_name = branch.tracking_branch().remote_name
        origin = repo.remote(name=remote_name)
        origin.pull(allow_unrelated_histories=True)
    return {'res': 1}


def sparta_317865cf5a(json_data, user_obj):
    """
    Push to remote repository
    """
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        branch = repo.active_branch
        remote_name = branch.tracking_branch().remote_name
        origin = repo.remote(name=f'{remote_name}')
        origin.push()
    return {'res': 1}


def sparta_18221e93ea(json_data, user_obj):
    """
    Pull repo
    """
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        for remote in repo.remotes:
            remote.fetch()
    return {'res': 1}


def sparta_ef1a55f717(json_data, user_obj):
    """
    Check if git repo created
    """
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    return {'res': 1, 'is_git_repository': is_git_repository}


def sparta_02ad92acd1(json_data, user_obj):
    """
    Load all commits
    """

    def get_commit_infos_dict(commit) ->dict:
        """
        Return git commit info for a specific commit
        """
        this_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(commit.committed_date))
        this_date = naturalday(parser.parse(str(this_time)))
        return {'author': commit.committer.name, 'author_name': commit.author.name, 'time': this_date, 'time_sort': this_time, 'sha':
            commit.hexsha, 'message': commit.message, 'summary': commit.summary
            }

    def get_git_commits_at_folder(folder_path) ->dict:
        """
        Function that returns all relevant information regarding commits, branches, remotes, commits behind, commits ahead..."""
        is_git_repository = sparta_15237d9e1c(folder_path)
        logger.debug(f'is_git_repository > {folder_path}')
        logger.debug(is_git_repository)
        if is_git_repository:
            repo = git.Repo(folder_path)
            commits_arr = []
            branches_arr = []
            for ref in repo.references:
                ref_name = ref.name
                branches_arr.append(ref_name)
                for commit in repo.iter_commits(rev=ref_name):
                    commitDict = get_commit_infos_dict(commit)
                    commitDict['branch'] = ref.name
                    commitDict['is_behind'] = 0
                    commitDict['is_ahead'] = 0
                    commits_arr.append(commitDict)
            commits_arr = sorted(commits_arr, key=lambda d: d['time_sort'],
                reverse=True)
            current_branch = repo.head.ref.name
            commits_behind_arr = []
            commits_ahead_arr = []
            if len(repo.remotes) > 0:
                branch = repo.active_branch
                remote_name = None
                tracking_branch = branch.tracking_branch()
                if tracking_branch is not None:
                    remote_branch = branch.tracking_branch().name
                    logger.debug(f'current_branch > {current_branch}')
                    logger.debug(f'remote_branch > {remote_branch}')
                    logger.debug('branch.tracking_branch()')
                    logger.debug(tracking_branch)
                    logger.debug(dir(tracking_branch))
                    logger.debug(tracking_branch.path)
                    logger.debug('Remote Name')
                    logger.debug(tracking_branch.remote_name)
                    remote_name = tracking_branch.remote_name
                    remote_branch_url = tracking_branch.config_reader()
                    logger.debug('remote_branch_url')
                    logger.debug(remote_branch_url)
                    try:
                        commits_behind = repo.iter_commits(
                            f'{current_branch}..{remote_branch}')
                        for this_commit_behind in commits_behind:
                            commitDict = get_commit_infos_dict(
                                this_commit_behind)
                            commits_behind_arr.append(commitDict)
                        logger.debug('commits_behind_arr')
                        logger.debug(commits_behind_arr)
                    except Exception as e:
                        logger.debug('Exception behind')
                        logger.debug(e)
                    try:
                        commits_ahead = repo.iter_commits(
                            f'{remote_branch}..{current_branch}')
                        for this_commit_ahead in commits_ahead:
                            commitDict = get_commit_infos_dict(
                                this_commit_ahead)
                            commits_ahead_arr.append(commitDict)
                        logger.debug('commits_ahead_arr')
                        logger.debug(commits_ahead_arr)
                    except Exception as e:
                        logger.debug('Exception Ahead')
                        logger.debug(e)
                    for thisCommitDict in commits_behind_arr:
                        this_sha = thisCommitDict['sha']
                        for thisCommitAll in commits_arr:
                            if thisCommitAll['branch'
                                ] == f'{remote_branch}' and thisCommitAll['sha'
                                ] == this_sha:
                                thisCommitAll['is_behind'] = 1
                                break
                    for thisCommitDict in commits_ahead_arr:
                        this_sha = thisCommitDict['sha']
                        for thisCommitAll in commits_arr:
                            if thisCommitAll['branch'
                                ] == current_branch and thisCommitAll['sha'
                                ] == this_sha:
                                thisCommitAll['is_ahead'] = 1
                                break
            remotes_arr = []
            for this_remote in repo.remotes:
                is_tracking = False
                logger.debug('----------------------------')
                logger.debug('this_remote')
                logger.debug(this_remote)
                logger.debug(dir(this_remote))
                if remote_name is not None:
                    if remote_name == this_remote.name:
                        is_tracking = True
                url = this_remote.config_reader.get('url')
                repo_name = os.path.splitext(os.path.basename(url))[0]
                domain_email = re.search('@[\\w.]+', url)
                if domain_email is not None:
                    domain_email = str(domain_email.group())
                    if domain_email.startswith('@'):
                        domain_email = domain_email[1:]
                else:
                    domain_email = ''
                remotes_arr.append({'name': this_remote.name, 'scm': url,
                    'repo_name': repo_name, 'domain': domain_email,
                    'is_tracking': is_tracking})
            logger.debug('remotes_arr')
            logger.debug(remotes_arr)
            is_base_directory = False
            if project_path == folder_path:
                is_base_directory = True
            return {'res': 1, 'is_base_directory': is_base_directory,
                'folder': folder_path, 'is_git_repo': is_git_repository,
                'commits_arr': commits_arr, 'branches': branches_arr,
                'current_branch': current_branch, 'remotes_arr':
                remotes_arr, 'commits_behind_arr': commits_behind_arr,
                'commits_ahead_arr': commits_ahead_arr}
    project_path = json_data['projectPath']
    res_dict = get_git_commits_at_folder(project_path)
    if res_dict is not None:
        res_dict['is_git_repo'] = True
        return res_dict
    else:
        return {'res': 1, 'is_git_repo': False}


def sparta_40e6ee6e8f(json_data, user_obj):
    """
    Get list of changed files (local) that need to be push to remote
    """
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        changed_files_arr = []
        for item in repo.index.diff(None):
            changed_files_arr.append({'file': item.a_path, 'change_type':
                item.change_type, 'is_deleted': item.deleted_file, 'path':
                item.a_path})
        untracked_files_arr = []
        for fileName in repo.untracked_files:
            untracked_files_arr.append({'file': fileName, 'path': fileName})
        return {'res': 1, 'changed_files_arr': changed_files_arr,
            'untracked_files_arr': untracked_files_arr}
    return {'res': 1}


def sparta_d40cb70f02(json_data, user_obj):
    """
    Run commit
    """
    project_path = json_data['projectPath']
    gitMsg = json_data['gitMsg']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        repo.git.add(all=True)
        repo.git.commit('-m', gitMsg)
    return {'res': 1}


@sparta_73d5f22424
def sparta_d6096c7033(json_data, user_obj):
    """
    Delete repository
    """
    return {'res': 1}


def sparta_3ac4ae3281(json_data, user_obj):
    """
    Delete Remote
    """
    logger.debug('Delete Remoete')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        scm = json_data['scm']
        for this_remote in repo.remotes:
            if scm == this_remote.config_reader.get('url'):
                repo.delete_remote(this_remote)
                break
    return {'res': 1}


def sparta_82eb26384a(json_data, user_obj):
    """
    Load all branches
    """
    return {'res': 1}


def sparta_8df26e4912(json_data, user_obj):
    """
    Create new branch
    """
    project_path = json_data['projectPath']
    branch_name = json_data['newBranchName']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        branch = [b for b in repo.branches if b.name == branch_name]
        if len(branch) == 0:
            original_branch = repo.active_branch
            branch = repo.create_head(branch_name)
            branch.checkout()
            repo.git.push('--set-upstream', 'origin', branch)
            original_branch.checkout()
            repo.git.checkout(branch_name)
            return {'res': 1}
        else:
            return {'res': -1, 'errorMsg':
                'A branch with this name already exists'}
    return {'res': -1, 'errorMsg':
        'An unexpected error occurred, please try again'}


def sparta_e2a7a6d25b(json_data, user_obj):
    """
    Checkout branch
    """
    project_path = json_data['projectPath']
    branch_name = json_data['branch2Checkout']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        try:
            repo.git.checkout(branch_name)
            return {'res': 1}
        except Exception as e:
            return {'res': -1, 'errorMsg': str(e)}
    return {'res': -1, 'errorMsg':
        'An unexpected error occurred, please try again'}


def sparta_4a50d341e1(json_data, user_obj):
    """
    Merge branch
    """
    project_path = json_data['projectPath']
    branch_name = json_data['branch2Merge']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        current_branch = repo.head.ref.name
        if current_branch == branch_name:
            return {'res': -1, 'errorMsg': 'Please choose another branch'}
        try:
            repo.git.checkout(branch_name)
            repo.git.merge(current_branch)
            return {'res': 1}
        except Exception as e:
            return {'res': -1, 'errorMsg': str(e)}
    return {'res': -1, 'errorMsg':
        'An unexpected error occurred, please try again'}


def sparta_6159113fd3(json_data, user_obj):
    """
    Delete branch
    """
    project_path = json_data['projectPath']
    branch_name = json_data['branch2Delete']
    is_git_repository = sparta_15237d9e1c(project_path)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        current_branch = repo.head.ref.name
        if current_branch == branch_name:
            return {'res': -1, 'errorMsg':
                'You cannot delete the active branch. Please checkout to another branch before deleting this one'
                }
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            os.chdir(project_path)
            proc = Popen(f'git branch -d {branch_name}', stdout=PIPE,
                stderr=PIPE, bufsize=1, universal_newlines=True, shell=True)
            read_lines = proc.stderr.readlines()
            proc = Popen(f'git push origin --delete {branch_name}', stdout=
                PIPE, stderr=PIPE, bufsize=1, universal_newlines=True,
                shell=True)
            read_lines = proc.stderr.readlines()
            os.chdir(dir_path)
            return {'res': 1}
        except Exception as e:
            return {'res': -1, 'errorMsg': str(e)}
    return {'res': -1, 'errorMsg':
        'An unexpected error occurred, please try again'}


def sparta_04a31d26b0(json_data, user_obj):
    """
    Load files diff
    """
    logger.debug('sqEditorGitLoadFilesDiff')
    logger.debug(json_data)
    project_path = json_data['projectPath']
    filename = json_data['filePath']
    fileType = json_data['fileType']
    is_git_repository = sparta_15237d9e1c(project_path)
    logger.debug('is_git_repository')
    logger.debug(is_git_repository)
    if is_git_repository:
        repo = git.Repo(project_path)
        sparta_e3a30d0668(repo, user_obj)
        diff_output = repo.git.diff()
        logger.debug('diff_output')
        logger.debug(diff_output)
        return {'res': 1, 'diff_output': diff_output}
    return {'res': -1, 'errorMsg':
        'An unexpected error occurred, please try again'}

#END OF QUBE
