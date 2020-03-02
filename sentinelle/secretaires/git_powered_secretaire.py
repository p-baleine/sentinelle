import contextlib
import datetime
import logging
import os
import re
import shutil
import time

from git import Repo

from sentinelle.secretaires.history import Difference, History


logger = logging.getLogger(__name__)

_WORKDIR_FORMAT = os.path.join(os.sep, 'tmp', 'sentinelle-worktree_{}')


class GitPoweredSecretaire(contextlib.ContextDecorator):

    def __init__(self, project_root_path=os.getcwd()):
        self._history = History()
        self.project_root_path = project_root_path
        self.work_dir = None
        self.rorepo = None
        self.latest_commit = None

    def record(self, report):   # 103
        self._apply_patch()
        self._update_latest_commit()

        logger.info('Diff are applied to working directory,'
                    ' current commit: {}'.format(self.latest_commit))

        self.history.append(
            passed=report.wasPassed(),
            content=report.getContent(),
            diff=self._create_diff())

    def __enter__(self):
        self.rorepo = Repo(self.project_root_path)

        assert self.rorepo.git.version_info > (2, 5, 1), (
           'worktree feature is not supported by your current git version,'
           ' so cannot make git-based history management enabled.')

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
        shutil.rmtree(self.work_dir)
        self.rorepo.git.worktree('remove', self.work_dir, '--force')
        self.rorepo.close()

    @property
    def history(self):
        return self._history

    def _create_diff(self):
        with self._wrepo() as wrepo:
            lhs, rhs = list(
                map(set, zip(
                    *[(d.a_path, d.b_path)
                      for d in wrepo.index.diff('HEAD@{1}')])))

            return Difference(
                commit=wrepo.git.rev_parse('HEAD'),
                previous=wrepo.git.rev_parse('HEAD@{1}'),
                changed_files=lhs | rhs,
                raw=wrepo.git.diff('HEAD^'),
                # TODO: deleted_file と new_file を実装する
                deleted_files=None, new_files=None)

    def _update_latest_commit(self):
        self.latest_commit = self._execute_git_command_on_work_dir(
            'rev-parse', 'HEAD')

    def _apply_patch(self):
        # Git の `user` セクションの設定がないとエラーになる
        # FIXME: diff がないと unrecognized input ってエラーになる

        pdiff = self.rorepo.git.diff(self.latest_commit, as_process=True)

        self._execute_git_command_on_work_dir(
            'apply', '-p1', '--directory', self.work_dir, '--unsafe-paths',
            istream=pdiff.stdout)

        # untracked ファイルもパッチ対象に含める
        untracked_files = self.rorepo.git.ls_files(
            '--others', '--exclude-standard')
        # FIXME: gitignore を反映する!!…とは言えバイナリだとパッチ適用できないのはなぜ？？
        untracked_files = [
            f for f in untracked_files.split('\n')
            if not re.match('work_tajima', f) and
            not re.match('envrc', f) and
            not re.match('poetry', f) and
            not re.match(r'.*(sentinelle|binlog|mysql\/(ebdb|ib_logfile)).*', f)]

        for f in untracked_files:
            pdiff = self.rorepo.git.diff(
                '/dev/null', f, as_process=True)
            self._execute_git_command_on_work_dir(
                'apply', '-p1', '--directory', self.work_dir, '--unsafe-paths',
                istream=pdiff.stdout)

        with self._wrepo() as wrepo:
            wrepo.git.add('-A')
            wrepo.git.commit('-m', 'Apply patch.')

    @contextlib.contextmanager
    def _wrepo(self):
        # FIXME: work_dir の .git とかで ResourceWarning がでている
        # ↓あたりが原因だと思っている
        # https://github.com/gitpython-developers/GitPython/blob/ff4f970fa426606dc88d93a4c76a5506ba269258/git/repo/fun.py#L60
        # でも、なぜ当該箇所でリソースの管理をしていないのか、分かっていない
        # …多分 GitPython の理解が乏しいため理解できていないんだと思う。
        # …どうでも良いけれど、ガンダムWのモビルスーツが外れなくダサくて好き
        repo = Repo(self.work_dir)

        try:
            yield repo
        finally:
            repo.close()

    def _execute_git_command_on_work_dir(self, *args, **kwargs):
        return self.rorepo.git.execute(
            ['git', '-C', self.work_dir] + list(args), **kwargs)
