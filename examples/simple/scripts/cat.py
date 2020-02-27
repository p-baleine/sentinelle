#!/usr/bin/env python

"""
cat.py - mimics cat(1).
"""

import argparse
import os
import sys

BASE_PATH = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(BASE_PATH))

from concatenate import concatenate  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('files', type=str, nargs='+')

if __name__ == '__main__':
    args = parser.parse_args()

    for line in concatenate(args.files).lines():
        sys.stdout.write(line)
