import sys
from pathlib import Path

print(f'cwd={Path.cwd()}')
for i, arg in enumerate(sys.argv[1:]):
    print(f'[{i}] ^{arg}$')
