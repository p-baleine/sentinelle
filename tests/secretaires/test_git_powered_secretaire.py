import contextlib
import io
import os
import tempfile
from textwrap import dedent
import time
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
        # あまり実行が早いと、work_dir の名前が被ってしまう
        # TODO: work_dir の名前に root ディレクトリの名前でも
        # 入れておけばよいのでは？；
        time.sleep(1)

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Repo.init(temp_dir)

            # 適当なファイルを編集
            with _readme(temp_dir, 'wt') as f1, _sister(temp_dir, 'wt') as f2:
                f1.write(dedent('''
                # Sample Project

                プレゼント・デイ
                '''))
                f2.write('ピーピー、がー')

            # commit しておく
            repo.index.add(os.path.join(temp_dir, 'README.md'))
            repo.index.commit('First commit.')

            with GitPoweredSecretaire(temp_dir) as secretaire:
                # unstaged な状態の変更をつくる
                # TODO: staged と committed な状態も検証する

                # 既存のファイルに対する変更
                with _readme(temp_dir, 'at') as f:
                    f.write(dedent('プレゼント・タイム'))

                # 新しいファイルを作る(untracked files)
                with _lain(temp_dir, 'wt') as f:
                    f.write(dedent('+ うるさいなぁ…黙ってられないの？？'))

                # 既存のお姉ちゃんを消す
                # TODO: むー、unstaged なファイルの削除は git diff に反映され
                # ないので、「変更のあったファイル一覧」に現状含めることができてない
                os.remove(os.path.join(temp_dir, 'sister.org'))

                previous_commit = secretaire.latest_commit
                previous_history_count = len(secretaire.history)
                report = _create_test_report()

                secretaire.record(report)

                # secretaire の管理する一時 worktree の latest_commitは
                # 変っているはず
                self.assertNotEqual(
                    secretaire.latest_commit, previous_commit)

                # オリジナル の commitは変っていないはず
                self.assertEqual(
                    repo.git.rev_parse('HEAD'), previous_commit)

                with contextlib.ExitStack() as stack:
                    # オリジナルのリポジトリと secretaire の管理する一時 worktree
                    # は、record 後は内容が一致していなくてはならない
                    src = stack.enter_context(_readme(temp_dir))
                    work = stack.enter_context(_readme(secretaire.work_dir))
                    self.assertEqual(src.readlines(), work.readlines())

                    # オリジナルで unstaged なファイルも secretaire の管理する一時
                    # worktree には保存されていなくてはならない
                    src2 = stack.enter_context(_lain(temp_dir))
                    work2 = stack.enter_context(_lain(secretaire.work_dir))

                    self.assertEqual(src2.readlines(), work2.readlines())

                    wrepo = Repo(secretaire.work_dir)

                    # work_dir における、今回分の差分
                    latest_diff = wrepo.git.diff('HEAD@{1}')
                    self.assertIn('+プレゼント・タイム', latest_diff)
                    self.assertIn('++ うるさいなぁ…黙ってられないの？？', latest_diff)

                    # 履歴の差分オブジェクトのチェック
                    latest_diff = secretaire.history.latest.diff
                    self.assertEqual(latest_diff.commit,
                                     wrepo.git.rev_parse('HEAD'))
                    self.assertEqual(latest_diff.previous,
                                     wrepo.git.rev_parse('HEAD@{1}'))
                    self.assertIn('README.md', latest_diff.changed_files)
                    self.assertIn('lain.org', latest_diff.changed_files)

                    self.assertIn('+プレゼント・タイム', latest_diff.raw)
                    self.assertIn('++ うるさいなぁ…黙ってられないの？？', latest_diff.raw)

            self.assertEqual(
                previous_history_count + 1, len(secretaire.history))
            self.assertEqual(
                'テストの結果に関する文字列だよ',
                secretaire.history.latest.content)

    def test_history(self):
        time.sleep(1)

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


def _lain(parent, mode='rt'):
    return open(os.path.join(parent, 'lain.org'), mode)


def _sister(parent, mode='rt'):
    return open(os.path.join(parent, 'sister.org'), mode)
