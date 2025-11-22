import os
import re
import shutil
import subprocess

url = 'https://gitlab.freedesktop.org/xorg/lib/libxcb-wm.git'
version = '0.4.2'
branch = 'xcb-util-wm-' + version
include_files = [line.strip() for line in open('files/include.txt')]
src_files = [line.strip() for line in open('files/src.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

with open('tmp/ewmh/atomlist.m4', 'r') as atoms_file:
    data = atoms_file.read()
    atoms = data[data.find('DO(') + 3: data.rfind(')')]
    atoms = [item.strip() for item in atoms.split(',')]

with open('tmp/ewmh/ewmh.c.m4', 'r') as file:
    data = '  \n' + ',\n'.join(
        f'  {{ sizeof("{i}") - 1, "{i}", offsetof(xcb_ewmh_connection_t, {i}) }}' for i in atoms
    )
    content = re.sub(r'.*?DO_ENTRY[\S\s]*?dnl\n', '', file.read())
    content = re.sub(r'dnl\n.*?dnl', data, content)
    with open('tmp/ewmh/ewmh.c', 'w') as new_file:
        new_file.write(content)

with open('tmp/ewmh/xcb_ewmh.h.m4', 'r') as file:
    data = '    \n' + '\n'.join(f'  xcb_atom_t {i};' for i in atoms)
    content = re.sub(r'dnl[\S\s]*dnl', data, file.read())
    with open('tmp/ewmh/xcb_ewmh.h', 'w') as new_file:
        new_file.write(content)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/COPYING')

os.makedirs('include/xcb', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/' + file, 'include/xcb/' + os.path.basename(file))

os.makedirs('src', exist_ok=True)
for file in src_files:
    shutil.copy2('tmp/' + file, 'src/' + os.path.basename(file))

with open('CMakeLists.txt', 'r+') as file:
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, file.read())
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
