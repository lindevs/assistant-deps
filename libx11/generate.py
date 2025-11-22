import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libx11.git'
version = '1.8.9'
branch = 'libX11-' + version
include_files = [line.strip() for line in open('files/include.txt')]
# The ks_tables.h file is produced by test-libx11.py and retrieved from a Docker container.
# Currently, there is no method to generate it directly on the Python side
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]
src_xcb_files = [line.strip() for line in open('files/src-xcb.txt')]
src_module_files = [line.strip() for line in open('files/src-module.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

for file in include_files:
    os.makedirs('include/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/include/' + file, 'include/' + file)

for file in include_private_files:
    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'include-private/' + file)

for file in src_files + src_xcb_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'src/' + file)

for file in src_module_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/' + file, 'src/' + file)

with open('tmp/include/X11/XlibConf.h.in', 'r+') as file:
    content = file.read().replace('#undef XTHREADS', '#cmakedefine XTHREADS @XTHREADS@')
    content = content.replace('#undef XUSE_MTSAFE_API', '#cmakedefine XUSE_MTSAFE_API @XUSE_MTSAFE_API@')
    if 'Generated' not in content:
        content = '/* include/X11/XlibConf.h.  Generated from XlibConf.h.in by configure.  */\n' + content
    file.seek(0)
    file.write(content)
    file.truncate()

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files + src_module_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
