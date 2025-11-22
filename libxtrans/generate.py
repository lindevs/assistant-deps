import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libxtrans.git'
version = '1.4.0'
branch = 'xtrans-' + version
include_files = [line.strip() for line in open('files/include.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

os.makedirs('include/X11/Xtrans', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/' + file, 'include/X11/Xtrans/' + file)

with open('CMakeLists.txt', 'r+') as file:
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, file.read())
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
