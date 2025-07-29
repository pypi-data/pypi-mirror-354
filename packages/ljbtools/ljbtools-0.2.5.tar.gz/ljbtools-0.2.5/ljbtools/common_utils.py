#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File    :   common_utils.py
# @Time    :   2025/06/09 17:07:30
# @Author  :   Jianbin Li
# @Version :   1.0
# @Contact :   jianbin0410@gmail.com
# @Desc    :   None

# here put the import lib
import os


def read_file(caller_path, file_path):
    _path = os.path.join(caller_path, file_path)
    with open(_path, 'r', encoding='utf-8') as f:
        return f.read()
