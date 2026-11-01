#!/usr/bin/env python3
"""Make OplTranC.exe: OPLTRAN.EXE with its .app output folder moved from the
read-only emulator Z: drive (\\epoc32\\release\\wins\\deb\\z\\) to C: (...\\c\\).
Run in epoc32/release/winc/deb of the OPL SDK."""
d = bytearray(open('OPLTRAN.EXE', 'rb').read())
old = b'\\epoc32\\release\\wins\\deb\\z\\System\\Apps\\'
new = b'\\epoc32\\release\\wins\\deb\\c\\System\\Apps\\'
i = d.find(old)
assert i > 0 and len(old) == len(new)
d[i:i + len(old)] = new
open('OplTranC.exe', 'wb').write(d)
print('patched at', hex(i))
