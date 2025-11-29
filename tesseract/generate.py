import os
import re
import shutil
import subprocess

url = 'https://github.com/tesseract-ocr/tesseract.git'
version = '5.5.1'
branch = version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_main_files = [line.strip() for line in open('files/src-main.txt')]
src_avx_files = [line.strip() for line in open('files/src-avx.txt')]
src_avx2_files = [line.strip() for line in open('files/src-avx2.txt')]
src_avx512_files = [line.strip() for line in open('files/src-avx512.txt')]
src_fma_files = [line.strip() for line in open('files/src-fma.txt')]
src_sse_files = [line.strip() for line in open('files/src-sse.txt')]
src_neon_files = [line.strip() for line in open('files/src-neon.txt')]
src_files = (src_main_files + src_avx_files + src_avx2_files + src_avx512_files + src_fma_files + src_sse_files
             + src_neon_files)

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

with open('tmp/src/ccutil/errcode.h', 'r+') as file:
    content = file.read().replace('in file %s, line %d", __FILE__', 'in function %s, line %d", __func__')
    file.seek(0)
    file.write(content)
    file.truncate()
with open('tmp/src/ccutil/unicharset.cpp', 'r+') as file:
    content = file.read().replace('__FILE__', '__func__')
    file.seek(0)
    file.write(content)
    file.truncate()

os.makedirs('license', exist_ok=True)
shutil.copy2('tmp/LICENSE', 'license/LICENSE')

os.makedirs('include/tesseract', exist_ok=True)
for file in include_files:
    shutil.copy2('tmp/include/tesseract/' + file, 'include/tesseract/' + file)

for file in include_private_files:
    os.makedirs('include-private/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'include-private/' + file)

for file in src_files:
    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2('tmp/src/' + file, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_main_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    src = ''.join(f'        src/{f}\n' for f in src_avx_files)
    content = re.sub(r'(set\(PROJECT_AVX_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_avx2_files)
    content = re.sub(r'(set\(PROJECT_AVX2_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_avx512_files)
    content = re.sub(r'(set\(PROJECT_AVX512_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_fma_files)
    content = re.sub(r'(set\(PROJECT_FMA_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_sse_files)
    content = re.sub(r'(set\(PROJECT_SSE_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_neon_files)
    content = re.sub(r'(set\(PROJECT_NEON_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
