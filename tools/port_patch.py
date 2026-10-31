#!/usr/bin/env python3
"""Patch VOYAGE5.OPL for the EPOC32 (Series 7) port. Keeps CRLF line endings.
- Data files live in the app's own folder on whatever drive it is installed on
  (the original hard-coded C:\\SYSTEM\\Apps\\voyage5, which breaks on a CF card).
- REGION=EU|US selects the ports database (the backup was left on US)."""
import sys, re
src, dst, region = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src, 'rb').read().decode('latin-1')
def sub(old, new, count=1):
    global t
    n = t.count(old)
    assert n >= count, (old, n)
    t = t.replace(old, new)
# app folder helper: derived from the running .app's path (CMD$(1))
sub('EXTERNAL Check$:', 'EXTERNAL Check$:\r\nEXTERNAL AppDir$:')
sub('const KUserFile$="C:\\SYSTEM\\Apps\\voyage5\\user"', 'REM\' EPOC port: user file and data directory are now AppDir$: (the app folder on its own drive)')
sub('const KFileDirectory$="C:\\SYSTEM\\Apps\\voyage5"', 'REM\'')
t = t.replace('KUserFile$', '(AppDir$:+"\\user")')
t = t.replace('KFileDirectory$', 'AppDir$:')
t += ('\r\nREM\' ==============================================================================================================\r\n'
      'PROC AppDir$:\r\n'
      'REM\' EPOC port: folder holding this .app, e.g. "D:\\SYSTEM\\APPS\\VOYAGE5" (no trailing backslash)\r\n'
      'LOCAL p$(255),i%\r\n'
      'p$=CMD$(1)\r\n'
      'i%=LEN(p$)\r\n'
      'WHILE i%>0 AND MID$(p$,i%,1)<>"\\"\r\n'
      '  i%=i%-1\r\n'
      'ENDWH\r\n'
      'IF i%<=1\r\n'
      '  RETURN "C:\\SYSTEM\\Apps\\voyage5"\r\n'
      'ENDIF\r\n'
      'RETURN LEFT$(p$,i%-1)\r\n'
      'ENDP\r\n')
if region == 'EU':
    sub('REM const kPORTF$="PORTS"', 'const kPORTF$="PORTS"')
    sub('const kPORTF$="USPORTS"', 'REM const kPORTF$="USPORTS"')
    sub('REM const kIPORT%=638', 'const kIPORT%=638')
    sub('REM const kCountryVer$="EUROPEAN Version"', 'const kCountryVer$="EUROPEAN Version"')
    sub('const kIPORT%=267', 'REM const kIPORT%=267')
    sub('const kCountryVer$="U.S.A Version"', 'REM const kCountryVer$="U.S.A Version"')
open(dst, 'wb').write(t.encode('latin-1'))
print('ok', region)
