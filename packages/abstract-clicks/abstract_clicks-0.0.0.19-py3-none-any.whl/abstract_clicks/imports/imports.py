import webbrowser
from PIL import Image
import pytesseract
import mss
import pyperclip
import time
import threading
import platform
import os
import subprocess
import time
import json
import math
import sys

from typing import (Any,
                    Dict,
                    List,
                    Optional,
                    Tuple
                    )
from abstract_utilities import (SingletonMeta,
                                safe_dump_to_file,
                                safe_load_from_file
                                )
from abstract_utilities.class_utils import get_class_inputs as get_inputs
from pynput import mouse, keyboard
from random import uniform
import base64
import uuid
import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/home/computron/miniconda/bin/tesseract'

# get a UUID - URL safe, Base64
import uuid

def get_uuid_id():
    return str(uuid.uuid4())
# ——— Globals ———
def get_abs_file():
    return os.path.abspath(__file__)
def get_abs_dir():
    abs_file = get_abs_file()
    return os.path.dirname(abs_file)
def get_abs_path(path):
    abs_dir = get_abs_dir()
    return os.path.join(abs_dir,path)
def get_abs_parent_path(path):
    abs_dir = get_abs_dir()
    dirname = os.path.dirname(abs_dir)
    return os.path.join(dirname,path)
def get_rel_dir():
    rel_dir = os.getcwd()
    return rel_dir
def get_rel_path(path):
    rel_dir = get_abs_dir()
    return os.path.join(rel_dir,path)

def get_events_path(path,default=None):
    path = path or default or "session.json"
    if os.path.exists(path):
        return path
    dirname = os.path.dirname(path)
    if dirname and os.path.isdir(dirname):
        return path
    return get_rel_path(path)
def get_time():
    return time.time()
def get_time_span(start_time):
    time_span = get_time() - start_time
    return time_span

def resolve_events_path(path, default=None):
    path = path or default or get_rel_path("session.json")
    dirname = os.path.dirname(path)
    if os.path.exists(path):
        return path
    dirname = os.path.dirname(path)
    if dirname and os.path.isdir(dirname):
        return path
    return get_rel_path(path)
def get_default_session_path():
    
    sessions_folder  = get_abs_parent_path('sessions')
    uuid = get_uuid_id()
    default_session_path = os.path.join(sessions_folder,f'{uuid}_default.json')
    return default_session_path
# Time utilities
def now() -> float:
    return time.time()

def elapsed(start: float) -> float:
    return now() - start
