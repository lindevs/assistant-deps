import os
import re
import shutil
import subprocess

url = 'https://github.com/PCRE2Project/pcre2.git'
version = '10.45'
branch = 'pcre2-' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
include_private_sljit_files = [line.strip() for line in open('files/include-private-sljit.txt')]
src_files = [line.strip() for line in open('files/src.txt')]
src_posix_files = [line.strip() for line in open('files/src-posix.txt')]
src_sljit_files = [line.strip() for line in open('files/src-sljit.txt')]

subprocess.check_call(
    ['git', 'clone', '--recursive', url, '--depth=1', '--branch=' + branch, 'tmp'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

shutil.copy2('tmp/src/pcre2.h.generic', 'tmp/src/pcre2.h')
shutil.copy2('tmp/src/pcre2_chartables.c.dist', 'tmp/src/pcre2_chartables.c')

os.makedirs('config', exist_ok=True)
shutil.copy2('tmp/config-cmake.h.in', 'config/config-cmake.h.in')

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENCE.md', 'license/LICENSE')

os.makedirs('include', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/src/' + file, 'include/' + file)

os.makedirs('include-private', exist_ok=True)
for file in include_private_files:
    shutil.copy2('tmp/src/' + file, 'include-private/' + file)

for file in include_private_sljit_files:
    shutil.copy2('tmp/deps/sljit/sljit_src/' + file, 'include-private/' + file)

os.makedirs('src', exist_ok=True)
for file in src_files + src_posix_files:
    path = 'tmp/src/' + file
    with open(path, 'r+') as new_file:
        content = new_file.read().replace('"../deps/sljit/sljit_src', '"sljit')
        new_file.seek(0)
        new_file.write(content)
        new_file.truncate()

    shutil.copy2(path, 'src/' + file)

for file in src_sljit_files:
    os.makedirs('src/sljit/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/deps/sljit/sljit_src/' + file, 'src/sljit/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_posix_files)
    content = re.sub(r'(set\(PROJECT_POSIX_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
