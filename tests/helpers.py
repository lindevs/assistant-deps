import os
import re
import subprocess
import filecmp
import shutil


def build_lib(lib, arch):
    os.makedirs('build/log', exist_ok=True)
    with open('build/log/' + lib + '-' + arch + '.txt', 'w') as file:
        subprocess.run(['tests/build/' + lib + '.sh', arch], check=True, stdout=file, stderr=file)


def ar_extract(lib, output):
    subprocess.check_call(['ar', '-x', lib, '--output', output])


def check_pkgconfig(lib, arch):
    passed = True
    for base_dir in ['lib', 'share']:
        ref_dir = 'build/lib/%s/%s/install/ref/%s/pkgconfig' % (lib, arch, base_dir)
        if os.path.isdir(ref_dir):
            break
    if not ref_dir:
        return passed

    for root, _, files in os.walk(ref_dir):
        for ref_name in files:
            ref_file = root + '/' + ref_name
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print('File not found: ' + file)
                passed = False
                continue

            with open(file, 'r+') as new_file:
                content = new_file.read().replace('/test', '/ref')
                new_file.seek(0)
                new_file.write(content)
                new_file.truncate()

            if not filecmp.cmp(ref_file, file):
                print('File not match: ' + file)
                passed = False
                continue

    for root, _, files in os.walk(ref_dir.replace('ref', 'test')):
        for name in files:
            file = root + '/' + name
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print('Unknown file: ' + file)
                passed = False
                continue

    return passed


def check_headers(lib, arch):
    passed = True
    include_dir = 'build/lib/%s/%s/install/ref/include' % (lib, arch)
    for root, _, files in os.walk(include_dir):
        for ref_name in files:
            ref_file = root + '/' + ref_name
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print('File not found: ' + file)
                passed = False
                continue
            if not filecmp.cmp(ref_file, file):
                print('File not match: ' + file)
                passed = False
                continue

    for root, _, files in os.walk(include_dir.replace('/ref/', '/test/')):
        for name in files:
            file = root + '/' + name
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print('Unknown file: ' + file)
                passed = False
                continue

    return passed


def check_libraries(lib, arch):
    passed = True
    lib_dir = 'build/lib/%s/%s/install/ref/lib' % (lib, arch)
    for root, _, files in os.walk(lib_dir):
        for ref_name in files:
            if not ref_name.endswith('.a'):
                continue
            ref_file = root + '/' + ref_name
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print('File not found: ' + file)
                passed = False
                continue
            if not check_object_files(ref_file, file):
                passed = False

    for root, _, files in os.walk(lib_dir.replace('/ref/', '/test/')):
        for name in files:
            if not name.endswith('.a'):
                continue
            file = root + '/' + name
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print('Unknown file: ' + file)
                passed = False
                continue

    return passed


def check_object_files(ref_lib, test_lib):
    passed = True

    ref_dir = '/tmp/obj/ref'
    test_dir = '/tmp/obj/test'

    os.makedirs(ref_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    ar_extract(ref_lib, ref_dir)
    ar_extract(test_lib, test_dir)

    for root, _, files in os.walk(ref_dir):
        for name in files:
            new_name = re.sub(r'.*?_la-', '', name).replace('.c.o', '.o')
            if name != new_name:
                os.rename(root + '/' + name, root + '/' + new_name)

    for root, _, files in os.walk(test_dir):
        for name in files:
            new_name = name.replace('.c.o', '.o')
            if name != new_name:
                os.rename(root + '/' + name, root + '/' + new_name)

    for root, _, files in os.walk(ref_dir):
        for ref_name in files:
            ref_file = root + '/' + ref_name
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print('File not found: ' + test_lib + ':' + file)
                passed = False
                continue
            if not filecmp.cmp(ref_file, file):
                print('File not match: ' + test_lib + ':' + file)
                passed = False
                continue

    for root, _, files in os.walk(test_dir):
        for name in files:
            file = root + '/' + name
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print('Unknown file: ' + file)
                passed = False
                continue

    shutil.rmtree('/tmp/obj')

    return passed
