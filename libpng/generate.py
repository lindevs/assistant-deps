import os
import re
import shutil
import subprocess

url = 'https://github.com/pnggroup/libpng.git'
version = '1.6.50'
branch = 'v' + version
include_files = [line.strip() for line in open('files/include.txt')]
include_private_files = [line.strip() for line in open('files/include-private.txt')]
src_main_files = [line.strip() for line in open('files/src-main.txt')]
src_intel_files = [line.strip() for line in open('files/src-intel.txt')]
src_arm_files = [line.strip() for line in open('files/src-arm.txt')]
src_mips_files = [line.strip() for line in open('files/src-mips.txt')]
src_powerpc_files = [line.strip() for line in open('files/src-powerpc.txt')]
src_loongarch_files = [line.strip() for line in open('files/src-loongarch.txt')]
src_riscv_files = [line.strip() for line in open('files/src-riscv.txt')]
src_files = (src_main_files + src_intel_files + src_arm_files + src_mips_files + src_powerpc_files + src_loongarch_files
             + src_riscv_files)

subprocess.check_call(['git', 'clone', url, '--depth=1', '--branch=' + branch, 'tmp'], stderr=subprocess.DEVNULL)

with open('tmp/scripts/pnglibconf.h.prebuilt', 'r') as file:
    content = file.read().replace('#define PNG_ZLIB_VERNUM 0 /* unknown */', '#define PNG_ZLIB_VERNUM 0x1310')
    with open('tmp/pnglibconf.h', 'w') as new_file:
        new_file.write(content)

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
    path = 'tmp/' + file
    with open(path, 'r+') as new_file:
        content = new_file.read().replace('#include "../', '#include "')
        new_file.seek(0)
        new_file.write(content)
        new_file.truncate()

    os.makedirs('src/' + os.path.dirname(file), exist_ok=True)
    shutil.copy2(path, 'src/' + file)

with open('CMakeLists.txt', 'r+') as file:
    src = ''.join(f'        src/{f}\n' for f in src_main_files)
    content = re.sub(r'(set\(PROJECT_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', file.read())
    src = ''.join(f'        src/{f}\n' for f in src_intel_files)
    content = re.sub(r'(set\(PROJECT_INTEL_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_arm_files)
    content = re.sub(r'(set\(PROJECT_ARM_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_mips_files)
    content = re.sub(r'(set\(PROJECT_MIPS_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_powerpc_files)
    content = re.sub(r'(set\(PROJECT_POWERPC_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_loongarch_files)
    content = re.sub(r'(set\(PROJECT_LOONGARCH_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    src = ''.join(f'        src/{f}\n' for f in src_riscv_files)
    content = re.sub(r'(set\(PROJECT_RISCV_SOURCES)[\S\s]*?\)', r'\g<1>\n' + src + ')', content)
    content = re.sub(r'(project\(.+? VERSION )[\d.]+', r'\g<1>' + version, content)
    file.seek(0)
    file.write(content)
    file.truncate()

shutil.rmtree('tmp')
