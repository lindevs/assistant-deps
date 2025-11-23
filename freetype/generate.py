import os
import re
import shutil
import subprocess

url = 'https://github.com/freetype/freetype.git'
version = '2.13.3'
branch = 'VER-' + version.replace('.', '-')
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_files = [line.strip() for line in open('files/src.txt')]
src_unix_files = [line.strip() for line in open('files/src-unix.txt')]

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

with open('tmp/include/freetype/config/ftoption.h', 'r+') as file:
    content = file.read()
    content = content.replace('/* #define FT_CONFIG_OPTION_SYSTEM_ZLIB */', '#define FT_CONFIG_OPTION_SYSTEM_ZLIB')
    content = content.replace('/* #define FT_CONFIG_OPTION_USE_PNG */', '#define FT_CONFIG_OPTION_USE_PNG')
    file.seek(0)
    file.write(content)
    file.truncate()

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE.TXT', 'license/LICENSE')

for file in include_files:
    os.makedirs('include/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/include/' + file, 'include/' + file)

for file in include_private_files:
    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    base_dir = 'include' if file.startswith('freetype') else 'src'
    shutil.copy2(('tmp/%s/' % base_dir) + file, 'include-private/' + file)

for file in src_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'src/' + file)

for file in src_unix_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/builds/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_unix_files)
    content = re.sub(r'(set\(PROJECT_UNIX_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
