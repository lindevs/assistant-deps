import sys
from time import time

from helpers import build_lib, check_headers, check_pkgconfig, check_libraries

start = time()
lib = sys.argv[1] if len(sys.argv) > 1 else quit(1)
arch = sys.argv[2] if len(sys.argv) > 2 else quit(1)
print('Checking ' + lib + '-' + arch)
build_lib(lib, arch)

passed = check_pkgconfig(lib, arch) and check_headers(lib, arch) and check_libraries(lib, arch)
extime = time() - start
print('%s-%s Passed (%.1fs)' % (lib, arch, extime) if passed else '%s-%s Failed (%.1fs)' % (lib, arch, extime))
