import os
import re
import shutil
import subprocess

url = 'https://github.com/webmproject/libwebp.git'
version = '1.6.0'
branch = 'v' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_main_files = [line.strip() for line in open('files/src-main.txt')]
src_sse_files = [line.strip() for line in open('files/src-sse.txt')]
src_avx2_files = [line.strip() for line in open('files/src-avx2.txt')]
src_sharpyuv_files = [line.strip() for line in open('files/src-sharpyuv.txt')]
src_mux_files = [line.strip() for line in open('files/src-mux.txt')]
src_demux_files = [line.strip() for line in open('files/src-demux.txt')]
src_decoder_files = [line.strip() for line in open('files/src-decoder.txt')]
src_files = src_main_files + src_sse_files + src_avx2_files + src_sharpyuv_files + src_mux_files + src_demux_files

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/COPYING', 'license/LICENSE')

for file in include_files:
    os.makedirs('include/webp/' + os.path.dirname(file), exist_ok=True)
    base_dir = '' if file.startswith('sharpyuv') else 'src/webp'
    shutil.copy2(('tmp/%s/' % base_dir) + file, 'include/webp/' + file)

for file in include_private_files:
    base_dir = '' if file.startswith('sharpyuv') else 'src'
    path = ('tmp/%s/' % base_dir) + file
    with open(path, 'r+') as new_file:
        content = new_file.read().replace('#include "src/', '#include "')
        new_file.seek(0)
        new_file.write(content)
        new_file.truncate()

    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2(path, 'include-private/' + file)

for file in src_files:
    base_dir = '' if file.startswith('sharpyuv') else 'src'
    path = ('tmp/%s/' % base_dir) + file
    with open(path, 'r+') as new_file:
        content = new_file.read().replace('#include "src/', '#include "')
        new_file.seek(0)
        new_file.write(content)
        new_file.truncate()

    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2(path, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_main_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_sse_files)
    content = re.sub(r'(set\(PROJECT_SSE_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_avx2_files)
    content = re.sub(r'(set\(PROJECT_AVX2_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_sharpyuv_files)
    content = re.sub(r'(set\(PROJECT_SHARPYUV_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_mux_files)
    content = re.sub(r'(set\(PROJECT_MUX_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_demux_files)
    content = re.sub(r'(set\(PROJECT_DEMUX_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_decoder_files)
    content = re.sub(r'(set\(PROJECT_DECODER_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
