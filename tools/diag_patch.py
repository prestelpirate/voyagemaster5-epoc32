#!/usr/bin/env python3
"""Diagnostic patch: number each start-up step and report the step, ERR and ERR$
in an alert if anything fails (Main had no error trap, so failures there gave
only the runtime's generic dialog)."""
import sys
f = sys.argv[1]
t = open(f, 'rb').read().decode('latin-1')
N = '\r\n'
def sub(old, new):
    global t
    assert old in t, old
    t = t.replace(old, new, 1)
sub('\tglobal ScrWid%', '\tglobal DiagStep%' + N + '\tglobal ScrWid%')
sub('\tREM\'Load the Bitmaps to use on the Toolbar into memory' + N + '    LoadToolBitMaps:',
    '\tONERR DiagTrap::' + N + '\tDiagStep%=1' + N + '    LoadToolBitMaps:')
sub('\tloadm "z:\\system\\opl\\Toolbar"', '\tDiagStep%=2' + N + '\tloadm "z:\\system\\opl\\Toolbar"' + N + '\tDiagStep%=3')
sub('\tTBarLink:("AppCont")' + N + N + 'endp',
    '\tTBarLink:("AppCont")' + N + '\tRETURN' + N + '\tDiagTrap::' + N + '\tONERR OFF' + N +
    '\tALERT("Main step "+GEN$(DiagStep%,4)+" error "+GEN$(err,6),err$(err))' + N + N + 'endp')
sub('\tEXTERNAL VY()               REM\' GLobal array of settings', '\tEXTERNAL VY()               REM\' GLobal array of settings' + N + '\tEXTERNAL DiagStep%')
# number the start-up calls inside AppCont (first occurrence of each, any indentation)
a = t.index('proc AppCont:')
b = t.index('\tdo' + N, a)
body = t[a:b].split(N)
want = {'gUpdate off': 10, 'initTBar:': 11, 'startScreen:': 12, 'getEvent32 event&()': 13,
        'ReadUser:': 14, 'ProcessCmdLine:': 15, 'OF:(1,0)': 16, 'DS:': 17, 'ToolBarButt:(KMainPage%)': 18}
out = []
for ln in body:
    k = ln.strip()
    if k in want:
        out.append('\tDiagStep%=' + str(want.pop(k)))
    out.append(ln)
assert not want, want
t = t[:a] + N.join(out) + t[b:]
sub('    ALERT("AppCont Error "+GEN$(err,10),err$(err))', '    ALERT("AppCont step "+GEN$(DiagStep%,4)+" error "+GEN$(err,10),err$(err))')
open(f, 'wb').write(t.encode('latin-1'))
print('diag ok')
