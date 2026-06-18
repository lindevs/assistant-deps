import os
import re
import subprocess
import filecmp
import hashlib


def build_lib(lib, arch):
    os.makedirs('build/log', exist_ok=True)
    with open(f'build/log/{lib}-{arch}.txt', 'w') as file:
        subprocess.run([f'tests/build/{lib}.sh', arch], check=True, stdout=file, stderr=file)


def get_object_files(lib):
    result = {}
    counts = {}
    lookup_data = b''

    with open(lib, 'rb') as f:
        if f.read(8) != b'!<arch>\n':
            raise ValueError('Invalid file')

        while True:
            header = f.read(60)
            if len(header) < 60:
                break

            raw_name = header[0:16].decode().rstrip()
            size = int(header[48:58].decode().rstrip())

            if raw_name == '/':
                f.seek(size + size % 2, 1)
            elif raw_name == '//':
                lookup_data = f.read(size)
                f.seek(size % 2, 1)
            else:
                if raw_name.startswith('/'):
                    offset = int(raw_name[1:])
                    org_name = lookup_data
                    for delim in (b'\x00', b'\x2F'):
                        pos = org_name.find(delim, offset)
                        if pos >= 0:
                            org_name = org_name[offset:pos]
                    org_name = org_name.decode()
                else:
                    org_name = raw_name.rstrip('/')

                name = re.sub(r'.*?_la-', '', org_name).removesuffix('.cpp.o').removesuffix('.c.o')
                name = name.removesuffix('.S.o').removesuffix('.o')
                name = name.removeprefix('meson-generated_').removeprefix('src_xkbcomp_').removeprefix('src_compose_')
                name = name.removeprefix('src_x11_').removeprefix('src_')

                counts[name] = counts.get(name, 0) + 1
                name = name if counts[name] == 1 else f'{name}_{counts[name]}'

                result[name] = hashlib.md5(f.read(size)).hexdigest()
                f.seek(size % 2, 1)

    return result


def check_pkgconfig(lib, arch):
    passed = True
    for base_dir in ['lib', 'share']:
        ref_dir = f'build/lib/{lib}/{arch}/install/ref/{base_dir}/pkgconfig'
        if os.path.isdir(ref_dir):
            break

    for root, _, files in os.walk(ref_dir):
        for ref_name in files:
            ref_file = f'{root}/{ref_name}'
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print(f'File not found: {file}')
                passed = False
                continue

            with open(ref_file, 'r') as f:
                ref_content = f.read()
            with open(file, 'r') as f:
                content = f.read().replace('/test', '/ref')
            if ref_content != content:
                print(f'File not match: {file}')
                passed = False

    for root, _, files in os.walk(ref_dir.replace('/ref/', '/test/')):
        for name in files:
            file = f'{root}/{name}'
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print(f'Unknown file: {file}')
                passed = False

    return passed


def check_headers(lib, arch):
    passed = True
    include_dir = f'build/lib/{lib}/{arch}/install/ref/include'
    for root, _, files in os.walk(include_dir):
        for ref_name in files:
            ref_file = f'{root}/{ref_name}'
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print(f'File not found: {file}')
                passed = False
                continue
            if not filecmp.cmp(ref_file, file, shallow=False):
                print(f'File not match: {file}')
                passed = False

    for root, _, files in os.walk(include_dir.replace('/ref/', '/test/')):
        for name in files:
            file = f'{root}/{name}'
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print(f'Unknown file: {file}')
                passed = False

    return passed


def check_libraries(lib, arch):
    passed = True
    lib_dir = f'build/lib/{lib}/{arch}/install/ref/lib'
    for root, _, files in os.walk(lib_dir):
        for ref_name in files:
            if not ref_name.endswith('.a'):
                continue
            ref_file = f'{root}/{ref_name}'
            file = ref_file.replace('/ref/', '/test/')
            if not os.path.isfile(file):
                print(f'File not found: {file}')
                passed = False
                continue
            if not check_object_files(ref_file, file):
                passed = False

    for root, _, files in os.walk(lib_dir.replace('/ref/', '/test/')):
        for name in files:
            if not name.endswith('.a'):
                continue
            file = f'{root}/{name}'
            ref_file = file.replace('/test/', '/ref/')
            if not os.path.isfile(ref_file):
                print(f'Unknown file: {file}')
                passed = False

    return passed


def check_object_files(ref_lib, test_lib):
    passed = True

    ref_objects = get_object_files(ref_lib)
    test_objects = get_object_files(test_lib)

    if len(ref_objects) != len(test_objects):
        print(f'Count not match:  {ref_lib} ({len(ref_objects)}) != {test_lib} ({len(test_objects)})')
        passed = False

    for name, digest in ref_objects.items():
        if name not in test_objects:
            print(f'Object not found: {test_lib}:{name}')
            passed = False
        elif digest != test_objects[name]:
            print(f'Object not match: {test_lib}:{name}')
            passed = False

    for name in test_objects:
        if name not in ref_objects:
            print(f'Object unknown:   {test_lib}:{name}')
            passed = False

    return passed
