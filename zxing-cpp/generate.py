import os
import re
import shutil
import subprocess

url = 'https://github.com/zxing-cpp/zxing-cpp.git'
version = '2.3.0'
branch = 'v' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

with open('tmp/core/src/Error.h', 'r+') as file:
    content = file.read().replace('__FILE__', '__func__')
    file.seek(0)
    file.write(content)
    file.truncate()

os.makedirs('config', exist_ok=True)
shutil.copy2('tmp/core/Version.h.in', 'config/Version.h.in')

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE', 'license/LICENSE')

os.makedirs('include/ZXing', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/core/src/' + file, 'include/ZXing/' + file)

for file in include_private_files:
    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/core/src/' + file, 'include-private/' + file)

for file in src_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/core/src/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
