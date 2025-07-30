import os
from pathlib import Path
from typing import Literal

def b_get_parent_dir(path: Literal['__file__']) -> Path:
    '''
    获取 该py文件 所在的文件夹
    :param path: __file__
    '''
    parent_dir = Path(path).parent
    return parent_dir

def b_get_cwd() -> Path:
    '''
    获取 当前工作目录current working directory
    '''
    return Path.cwd()