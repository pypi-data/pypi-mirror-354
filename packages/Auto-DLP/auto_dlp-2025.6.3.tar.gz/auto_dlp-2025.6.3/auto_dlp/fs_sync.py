import os.path as path
import shutil
from pathlib import Path
import pycopy

import auto_dlp.utils as utils
from auto_dlp import terminal_formatting

def sync(src, dest):
    pycopy.sync(src, dest, do_delete=True)