import os
import re
import shutil
import subprocess

# The parser.c and parser.h files are produced by Bison and retrieved from a Docker container.
# Currently, there is no method to generate it directly on the Python side

url = 'https://github.com/xkbcommon/libxkbcommon.git'
version = '1.10.0'
branch = 'xkbcommon-' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_main_files = [line.strip() for line in open('files/src-main.txt')]
src_x11_files = [line.strip() for line in open('files/src-x11.txt')]
src_files = src_main_files + src_x11_files

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE', 'license/LICENSE')

os.makedirs('include/xkbcommon', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/include/xkbcommon/' + file, 'include/xkbcommon/' + file)

for file in include_private_files:
    path = 'tmp/src/' + file
    with open(path, 'r+') as new_file:
        content = new_file.read().replace('#include "src/', '#include "')
        content = content.replace('#include "parser.h"', '#include "bison/parser.h"')
        new_file.seek(0)
        new_file.write(content)
        new_file.truncate()

    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2(path, 'include-private/' + file)

for file in src_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_main_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_x11_files)
    content = re.sub(r'(set\(PROJECT_X11_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
