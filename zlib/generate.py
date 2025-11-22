import os
import re
import shutil
import subprocess

url = 'https://github.com/madler/zlib.git'
version = '1.3.1'
branch = 'v' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('config', exist_ok=True)
shutil.copy2('tmp/zconf.h.cmakein', 'config/zconf.h.cmakein')

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE', 'license/LICENSE')

os.makedirs('include', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/' + file, 'include/' + file)

os.makedirs('include-private', exist_ok=True)
for file in include_private_files:
    shutil.copy2('tmp/' + file, 'include-private/' + file)

os.makedirs('src', exist_ok=True)
for file in src_files:
    shutil.copy2('tmp/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
