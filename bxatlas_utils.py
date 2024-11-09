import bpy
import os

import os
import platform

import ctypes
from ctypes import *


def fix_dir_path(dir_path):
    dir_path = dir_path.replace('\\', '/')
    if not dir_path.endswith('/'):
        dir_path += '/'

    return dir_path


def get_addon_dir():
    # base_path = os.path.realpath(__file__)
    # base_path = os.path.dirname(base_path)

    base_path = os.path.dirname(__file__)
    base_path = fix_dir_path(base_path)

    return base_path


def load_xatlas():
    platfm = platform.system()

    if platfm == 'Windows':  # Windows
        bxatlas = ctypes.CDLL(get_addon_dir() + "BXAtlas_CTypes/build/Release/BXAtlas.dll")
    elif platfm == 'Darwin':  # MacOS
        bxatlas = ctypes.CDLL(get_addon_dir() + "BXAtlas_CTypes/build/Release/BXAtlas.dylib")
    else:  # Linux
        bxatlas = ctypes.CDLL(get_addon_dir() + "BXAtlas_CTypes/build/Release/BXAtlas.so")

    return bxatlas