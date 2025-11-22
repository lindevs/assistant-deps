import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libxcb-render-util.git'
version = '0.3.10'
branch = 'xcb-util-renderutil-' + version
include_files = [line.strip() for line in open('files/include.txt')]
src_files = [line.strip() for line in open('files/src.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

os.makedirs('include/xcb', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/renderutil/' + file, 'include/xcb/' + file)

os.makedirs('src', exist_ok=True)
for file in src_files:
    shutil.copy2('tmp/renderutil/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
