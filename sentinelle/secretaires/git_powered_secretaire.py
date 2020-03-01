from contextlib import ContextDecorator
import datetime
from git import Repo
import logging
import os
import time

from sentinelle.secretaires.history import History


logger = logging.getLogger(__name__)

_WORKDIR_FORMAT = os.path.join(os.sep, 'tmp', 'sentinelle-worktree_{}')


class GitPoweredSecretaire(ContextDecorator):

    def __init__(self, project_root_path=os.getcwd()):
        self._history = History()
        self.rorepo = Repo(project_root_path)
        self.work_dir = None
        self.latest_commit = None

        assert self.rorepo.git.version_info > (2, 5, 1), (
           'worktree feature is not supported by your current git version,'
           ' so cannot make git-based history management enabled.')

    def record(self, report):
        self._apply_patch()
        self._update_latest_commit()

        logger.info('The diff are applied to working directory,'
                    ' current commit: {}'.format(self.latest_commit))

        self.history.append(
            passed=report.wasPassed(),
            content=report.getContent(),
            diff=None)

    def __enter__(self):
        now = time.time()
        ts = datetime.datetime.fromtimestamp(now).strftime('%Y%m%d%H%M%S')
        self.work_dir = _WORKDIR_FORMAT.format(ts)
        self.rorepo.git.worktree('add', self.work_dir, '--detach')

        logger.info('Add a temporal detached worktree'
                    'at "{}"'.format(self.work_dir))

        self._update_latest_commit()

        return self

    def __exit__(self, exc_type, exc, exc_tb):
        logger.info(
            'Remove temporary working directory, {}'.format(self.work_dir))
        self.rorepo.git.worktree('remove', self.work_dir, '--force')

    @property
    def history(self):
        return self._history

    def _update_latest_commit(self):
        self.latest_commit = self._execute_git_command_on_work_dir(
            'rev-parse', 'HEAD')

    def _apply_patch(self):
        pdiff = self.rorepo.git.diff(self.latest_commit, as_process=True)
        self._execute_git_command_on_work_dir(
            'apply', '-p1', '--directory', self.work_dir, '--unsafe-paths',
            istream=pdiff.stdout)
        self._execute_git_command_on_work_dir('add', '-A')
        self._execute_git_command_on_work_dir(
            'commit', '-m', 'Apply patch.')

    def _execute_git_command_on_work_dir(self, *args, **kwargs):
        return self.rorepo.git.execute(
            ['git', '-C', self.work_dir] + list(args), **kwargs)
