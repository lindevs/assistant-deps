import os
import re
import shutil
import subprocess

url = 'https://github.com/libffi/libffi.git'
version = '3.5.2'
branch = 'v' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
include_private_target_files = [line.strip() for line in open('files/include-private-target.txt')]
src_main_files = [line.strip() for line in open('files/src-main.txt')]
src_x86_64_files = [line.strip() for line in open('files/src-x86-64.txt')]
src_aarch64_files = [line.strip() for line in open('files/src-aarch64.txt')]
src_riscv_files = [line.strip() for line in open('files/src-riscv.txt')]
src_files = src_main_files + src_x86_64_files + src_aarch64_files + src_riscv_files

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('config', exist_ok=True)
shutil.copy2('tmp/include/ffi.h.in', 'config/ffi.h.in')

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE', 'license/LICENSE')

for file in include_files:
    os.makedirs('include/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'include/' + file)

os.makedirs('include-private', exist_ok=True)
for file in include_private_files:
    shutil.copy2('tmp/include/' + file, 'include-private/' + file)

for file in include_private_target_files:
    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'include-private/' + file)

for file in src_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_main_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_x86_64_files)
    content = re.sub(r'(set\(PROJECT_X86_64_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_aarch64_files)
    content = re.sub(r'(set\(PROJECT_AARCH64_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_riscv_files)
    content = re.sub(r'(set\(PROJECT_RISCV_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
