import os
import glob
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/proto/xorgproto.git'
include_files = [line.strip() for line in open('files/include.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
for file_path in glob.glob('tmp/COPYING*'):
    shutil.copy2(file_path, 'license/' + os.path.basename(file_path))

os.makedirs('config', exist_ok=True)
shutil.copy2('tmp/include/X11/Xpoll.h.in', 'config/Xpoll.h.in')

for file in include_files:
    os.makedirs('include/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/include/' + file, 'include/' + file)

shutil.rmtree('tmp')
