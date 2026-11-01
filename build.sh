#!/bin/bash
# Build VoyageMaster 5 for the Psion Series 7 (ER5) with the OPL SDK's OPLTRAN under wine.
#   OPLSDK=/path/to/opl  ./build.sh [EU|US ...]      (default: EU US)
# OPLSDK is the "opl" folder from the Psion OPL SDK (opl.zip), mapped to wine drive Y:.
# OPLTRAN always writes .app files to its read-only emulator Z: drive; tools/patch_opltran.py
# makes OplTranC.exe, which writes to ...\wins\deb\c\System\Apps instead.
# DIAG=1 adds start-up step reporting (tools/diag_patch.py).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
OPLSDK=${OPLSDK:-$HOME/opl_sdk/opl}
REGIONS=${*:-EU US}
ln -sfn "$OPLSDK" "$HOME/.wine/dosdevices/y:"
ln -sfn "$HERE" "$OPLSDK/work"
W=$OPLSDK/Epoc32/Release/Winc/Deb
[ -f "$W/OplTranC.exe" ] || (cd "$W" && python3 "$HERE/tools/patch_opltran.py")
mkdir -p "$OPLSDK/Epoc32/Release/Wins/Deb/c/System/Apps" "$HERE/build" "$HERE/dist"
OUT=$OPLSDK/Epoc32/Release/Wins/Deb/c/System/Apps/VOYAGE5
for R in $REGIONS; do
  python3 "$HERE/tools/port_patch.py" "$HERE/src/VOYAGE5.OPL" "$HERE/build/VOYAGE5.OPL" $R
  [ "$DIAG" = 1 ] && python3 "$HERE/tools/diag_patch.py" "$HERE/build/VOYAGE5.OPL"
  cp "$HERE"/src/*.OPH "$HERE"/src/*.OXH "$HERE/build/"
  rm -rf "$OUT"
  (cd "$OPLSDK" && wine 'y:\epoc32\release\winc\deb\OplTranC.exe' -e 'y:\work\build\VOYAGE5.OPL' 2>&1 | grep -v -i 'winediag\|systray\|explorer\|fixme') | tee /tmp/opltran.log
  grep -q 'translated OK' /tmp/opltran.log
  S=$HERE/dist/$R; rm -rf "$S"; A=$S/System/Apps/Voyage5; mkdir -p "$A" "$S/System/Opx"
  cp "$OUT/VOYAGE5.app" "$A/Voyage5.app"; cp "$OUT/VOYAGE5.aif" "$A/Voyage5.aif"
  cp "$HERE/data/VOY5BAR.MBM" "$A/Voy5Bar.mbm"; cp "$HERE/data/VOYAGE.HLP" "$A/Voyage.hlp"
  if [ $R = EU ]; then cp "$HERE/data/PORTS.DAT" "$A/Ports.dat"; else cp "$HERE/data/USPORTS.DAT" "$A/USPorts.dat"; fi
  cp "$HERE/data/SYSRAM1.OPX" "$S/System/Opx/SysRam1.opx"
done
ls -la "$HERE"/dist/*/System/Apps/Voyage5/Voyage5.app
