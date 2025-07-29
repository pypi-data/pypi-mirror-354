from PIL import Image
import pytesseract
import mss
import pyperclip
import pyautogui
import time
import threading
import platform
import os
import subprocess
import os
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
from pynput import mouse, keyboard
from random import uniform
