import contextlib
import io
import os
import tempfile
from textwrap import dedent
import unittest
from unittest.runner import TextTestResult

from git import Repo

from sentinelle.inspectors.inspection_report import TextInspectionReport
from sentinelle.secretaires import History, GitPoweredSecretaire


def _create_test_report():
    stream = io.StringIO()
    stream.write('テストの結果に関する文字列だよ')
    return TextInspectionReport(TextTestResult(
        stream=stream,
        descriptions="",
        verbosity=1,
    ))


class GitPoweredSecretaierTest(unittest.TestCase):

    def test_record(self):
        # テスト用の一時ディレクトリを作る
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Repo.init(temp_dir)

            # 適当なファイルを add して
            with _readme(temp_dir, 'wt') as f:
                f.write(dedent('''
                # Sample Project

                プレゼント・デイ
                '''))

            # commit しておく
            repo.index.add(os.path.join(temp_dir, 'README.md'))
            repo.index.commit('First commit.')

            with GitPoweredSecretaire(temp_dir) as secretaire:
                # unstaged な状態の変更をつくる
                # TODO: staged と committed な状態も検証する

                with _readme(temp_dir, 'at') as f:
                    f.write(dedent('''
                    プレゼント・タイム
                    '''))

                previous_commit = secretaire.latest_commit
                previous_history_count = len(secretaire.history)
                report = _create_test_report()

                secretaire.record(report)

                with contextlib.ExitStack() as stack:
                    src = stack.enter_context(_readme(temp_dir))
                    work = stack.enter_context(_readme(secretaire.work_dir))
                    # オリジナルのリポジトリと secretaire の管理する一時 worktree
                    # は、record 後は内容が一致していなくてはならない
                    self.assertEqual(src.readlines(), work.readlines())

                    # secretaire の管理する一時 worktree の latest_commitは
                    # 変っているはず
                    self.assertNotEqual(
                        secretaire.latest_commit, previous_commit)

                    # オリジナル の commitは変っていいないはず
                    self.assertEqual(
                        repo.git.rev_parse('HEAD'), previous_commit)

                    # TODO: 一つまえのコミットは前回のもののはず
                    # TODO: history には今回実行分の結果が入っているはず

            self.assertEqual(
                previous_history_count + 1, len(secretaire.history))
            self.assertEqual(
                'テストの結果に関する文字列だよ',
                secretaire.history.latest.content)

    def test_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Repo.init(temp_dir)

            with _readme(temp_dir, 'wt') as f:
                f.write(dedent('はははは'))

            repo.index.add(os.path.join(temp_dir, 'README.md'))
            repo.index.commit('First commit.')

            with GitPoweredSecretaire(temp_dir) as secretaire:
                self.assertIsInstance(secretaire.history, History)


def _readme(parent, mode='rt'):
    return open(os.path.join(parent, 'README.md'), mode)
