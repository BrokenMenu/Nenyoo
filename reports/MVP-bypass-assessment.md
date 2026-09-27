# Nenyoo MVP BattlEye bypass assessment: Enhanced and Legacy

**Verdict: a working BattlEye bypass has not been established. The captured MVP files contain no executable content beyond their matching VIP files.** This does not establish that a shared or externally controlled bypass is absent. The injection mechanism and reasons for reported bans remain unverified.

This expanded offline review rechecked both MVP editions against the preserved VIP baselines. It read files without executing them, contacting menu servers, attaching a debugger, extracting a bypass component or modifying anti-cheat protections. MVP tier attribution remains based on the reported selection and changed cache artifact; live module enumeration was unavailable for these two captures.

## Fresh comparison results

| Check | MVP Enhanced | MVP Legacy |
| --- | --- | --- |
| Original packed MVP contains complete VIP file unchanged | Yes | Yes |
| Decompressed MVP contains complete VIP file unchanged | Yes | Yes |
| Additional bytes, in both forms | 2,334 | 2,675 |
| Every additional byte is ASCII space (`0x20`) | Yes | Yes |
| Decompressed sections matching VIP | 9 of 9 | 9 of 9 |
| Additional executable section or code in the tail | None | None |
| PE identity | Native x64 DLL | Native x64 DLL |
| Imported DLL descriptors | 31 | 31 |
| Imported functions | 642 | 641 |

Fresh whole-file hashes matched the [preserved artifact manifest](../evidence/artifact-manifest.json). Because the entire corresponding VIP file is an unchanged prefix, headers, executable sections, import tables and file-backed data within that prefix are also unchanged. The padding has no distinct executable contents. Its runtime purpose is not established.

## Selected imports and direct-reference check

Both MVP images import DeviceIoControl, OpenProcess, ReadProcessMemory, LoadLibraryA and GetProcAddress. The selected static checks found no imports for NtLoadDriver/ZwLoadDriver, their unload counterparts, CreateService/StartService, OpenSCManager/OpenService, ControlService or DeleteService.

The presence of DeviceIoControl is a device-communication capability. It does not identify a cheat driver, the contacted device, an IOCTL's purpose, or whether the call executes.

An additional linear x64 disassembly of executable file-backed sections counted direct RIP-relative call/jump references to selected import-address-table slots:

| Imported API | MVP Enhanced static references | MVP Legacy static references |
| --- | ---: | ---: |
| DeviceIoControl | 3 | 3 |
| OpenProcess | 4 | 4 |
| ReadProcessMemory | 5 | 5 |
| LoadLibraryA | 24 | 22 |
| GetProcAddress | 46 | 47 |

These are **static references, not observed executed calls**. The scan covered 10,811,392 executable file-backed bytes in Enhanced and 10,909,696 in Legacy, including 2,194 and 2,134 bytes handled as undecodable data respectively. Linear interpretation can confuse embedded data with instructions and does not resolve indirect wrappers, computed pointers, runtime state, dynamic API resolution or downloaded components. No implementation or instruction listing is exported. The references cannot be classified as a functioning bypass from these counts.

## Text indicators

Case-insensitive selected ASCII/UTF-16 checks found 11 ASCII occurrences of BattlEye and 13 of bypass in each decompressed MVP DLL. No matches were found for BattleEye, BEDaisy or BEService. The first offsets agree with the [earlier reference check](../evidence/battleye-reference-check.json).

Separate word matches do not establish their relation, executed feature state or a working bypass. These bytes also exist in the corresponding VIP prefix, so they are not MVP-exclusive content.

## Runtime and ban-cause limits

The separate runtime trace recorded the cached menu DLL loading into the loader and GTA. No new conventional kernel image load appeared in retained events. The observed driver unload was existing BEDaisy.sys after GTA ended. That trace was not independently tier-labeled MVP and omitted approximately 3.1 seconds of loader startup. It cannot rule out a temporary component in the missing interval, assistance from an existing driver or an unconventional mechanism. See [the runtime assessment](runtime-driver-assessment.md).

No controlled validation of the reported MVP protected-online functionality was performed. No ban decision records, detection explanations or correlated affected-player cases were provided. Therefore the evidence does not support the claim that user-mode injection caused particular bans. Kernel status alone does not establish a bypass's presence, effectiveness or safety.

Rockstar's [GTA Online BattlEye FAQ](https://support.rockstargames.com/articles/1nenwhZlVrJY6CTFeSS2Fx/grand-theft-auto-online-battleye-faq) describes monitoring that includes processes, drivers and executable code, and says detected cheat software can lead to account action. That general description does not identify what triggered any particular ban or establish that every claimed bypass requires kernel injection.

## Reproducible evidence

- [Fresh MVP static results](../evidence/MVP-bypass-static-recheck.json): hashes, section metadata, selected imports, direct-reference counts and literal offsets.
- [Read-only assessment script](../tools/assess_mvp.py): repeat with Python; add `--with-capstone` if the capstone package is available to include the limited disassembly check.
- [Artifact verifier](../tools/verify_artifacts.py): whole-file hashes and exact VIP/MVP prefix/padding checks.
- [Full section comparison](../evidence/All-variants-comparison.json): matching section hashes and edition differences.

The reported MVP promise was supplied by the operator. An independently archived vendor advertisement and a demonstrated feature test are not part of this evidence set. The result is unverified functionality, not a proven finding of fraud.
