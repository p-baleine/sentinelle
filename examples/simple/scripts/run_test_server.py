import logging
import os
import sys


# TODO: 後で消す、sentinelle 自体へのパスを追加
SENTINELLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, os.path.join(SENTINELLE_PATH))

# 通常 python -m unittest tests/test_concatenenate.py だと実行した場所から
# 引数のファイルをひいてこれるけど、このスクリプト(scripts/ 配下)からだと
# tests/test_concatenenate.py が見えない。そのためtests ディレクトリを参照する
# ためにexamples/simple のパスを追加している
# NOTE: 多分、simpleな場合や Django 版の場合は、この処理をコマンドにできる
# どこに tests ディレクトリが存在するかはプロジェクトに依存する。
# 例えば、テストのディレクトリを引数にとるようなコマンドを用意すれば良いかと思う。
BASE_PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(BASE_PATH))

# NOTE: 変更のあったソースは reload しないとだめ
# + テスト対象に変更があったとき、ちゃんとリロードされる？
# + テストコードに変更があったとき、ちゃんとリロードされる？


# TODO: Django とかで見かける manager.py パターンを検討する
# あっちがスタンダードならそれにのっかりたい…んだけど、Django とか既に
# manager.py は存在するためそこは工夫が必要そう

import sentinelle  # noqa: E402

if __name__ == '__main__':
    logging.basicConfig()
    inspector = sentinelle.inspectors.BareUnittestInspector()
    sentinelle.serve(avec=inspector)
