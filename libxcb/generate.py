import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libxcb.git'
version = '1.17.0'
branch = 'libxcb-' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]
src_component_files = [line.strip() for line in open('files/src-component.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)
subprocess.check_call(
    ['git', 'clone', 'https://gitlab.freedesktop.org/xorg/proto/xcbproto.git', '--depth=1', 'tmp/xcbproto'],
    stderr=subprocess.DEVNULL
)

shutil.copytree('tmp/xcbproto/xcbgen', 'tmp/src/xcbgen', dirs_exist_ok=True)
shutil.copytree('tmp/xcbproto/src', 'tmp/src/xml', dirs_exist_ok=True)

for root, _, files in os.walk('tmp/src/xml'):
    for name in files:
        if name.endswith('.xml'):
            subprocess.check_call(
                [
                    'python3', 'c_client.py',
                    '-c', 'libxcb',
                    '-l', 'X Version 11',
                    '-s', '3',
                    '-p', 'xcbproto',
                    (root + '/' + name).lstrip('tmp/src/')
                ],
                cwd='tmp/src'
            )

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

os.makedirs('include/xcb', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/src/' + file, 'include/xcb/' + file)

os.makedirs('include-private', exist_ok=True)
for file in include_private_files:
    shutil.copy2('tmp/src/' + file, 'include-private/' + file)

os.makedirs('src', exist_ok=True)
for file in src_files:
    shutil.copy2('tmp/src/' + file, 'src/' + file)

for file in src_component_files:
    shutil.copy2('tmp/src/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
