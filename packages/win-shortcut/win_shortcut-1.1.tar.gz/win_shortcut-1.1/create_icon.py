import sys
from pathlib import Path

import win_shortcut

win_shortcut.create_shortcut(win_shortcut.get_known_folder(win_shortcut.KnownFolderId.Desktop), [sys.executable, 'print_args.py', 'hello', 'world'], icon=win_shortcut.pifmgr.RACECAR)
