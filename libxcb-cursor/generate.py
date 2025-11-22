import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libxcb-cursor.git'
version = '0.1.5'
branch = 'xcb-util-cursor-' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

os.makedirs('include/xcb', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/cursor/' + file, 'include/xcb/' + file)

os.makedirs('include-private', exist_ok=True)
for file in include_private_files:
    shutil.copy2('tmp/cursor/' + file, 'include-private/' + file)

os.makedirs('src', exist_ok=True)
for file in src_files:
    shutil.copy2('tmp/cursor/' + file, 'src/' + file)

# The shape_to_id.c file is produced by test-libxcb-cursor.py and retrieved from a Docker container.
# Currently, there is no method to generate it directly on the Python side
src_files.append('shape_to_id.c')

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
