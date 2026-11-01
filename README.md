# VoyageMaster 5 for the Psion Series 7 (EPOC ER5)

VoyageMaster 5 (version 1.08) is a voyage and tide planning program for the Psion Series 5,
written in OPL by Dolphin Maritime Software (1997–98). This repository is a port of it to the
**Psion Series 7** (and netBook), with a build that runs on Linux.

## Builds

Each release has one build per ports database:

| Zip | Ports database | Machines | Status |
|---|---|---|---|
| `voyagemaster5-1.08-series7-europe.zip` | European (`Ports.dat`, 638 ports) | Psion Series 7 | **Tested** on a Series 7 |
| `voyagemaster5-1.08-series7-usa.zip` | USA (`USPorts.dat`, 267 ports) | Psion Series 7 | **Not tested** (same program, different ports file) |

Install only one at a time: both use the same application folder and UID.

## Installing

1. Download the zip from the [Releases](../../releases) page.
2. Extract it **to the root of a CompactFlash card** (or to the root of the C: drive).
   This creates `\System\Apps\Voyage5\` (`Voyage5.app`, `Voyage5.aif`, `Voy5Bar.mbm`,
   `Voyage.hlp` and the ports file) and `\System\Opx\SysRam1.opx`.
3. VoyageMaster appears on the Extras bar as **Voyage5**. Tap it to start.

Tide data, user settings and own-port files are kept in `\System\Apps\Voyage5\` on the drive the app is installed on.
Documents are created in `C:\Documents`.

## Changes from the Series 5 original

- Data files and the user file are found in the app's own folder on whatever drive it is on
  (the original hard-coded `C:\SYSTEM\Apps\voyage5`, which fails when installed on a CF card).
- The European or US ports database is chosen at build time (the source was last left on US).
- No other changes to the program. The screen layout is still the Series 5 640×240 one.

## Building from source

Requirements: wine, Python 3, and the Psion **OPL SDK** (the `opl` folder from `opl.zip`).

```sh
OPLSDK=/path/to/opl ./build.sh          # both regions -> dist/EU and dist/US
OPLSDK=/path/to/opl ./build.sh EU       # European only
DIAG=1 OPLSDK=/path/to/opl ./build.sh   # with start-up step error reporting
```

The SDK's `OPLTRAN.EXE` writes translated apps only to the emulator's read-only Z: drive.
`tools/patch_opltran.py` makes a copy, `OplTranC.exe`, that writes to C: instead.

| Path | Contents |
|---|---|
| `src/VOYAGE5.OPL` | Original OPL source (unchanged from the 11-97 backup apart from the icon path) |
| `src/*.OPH`, `src/SYSRAM1.OXH` | Include files used by the source |
| `tools/port_patch.py` | Applies the Series 7 changes to a copy of the source at build time |
| `tools/diag_patch.py` | Optional start-up step reporting |
| `icon/Voyage5.mbm` | Application icon |
| `data/` | Toolbar bitmaps, help file, ports databases and `SYSRAM1.OPX` |

## Licence

VoyageMaster 5 is copyright (c) Dolphin Maritime Software. All rights reserved.
