# Nenyoo loader analysis: user-mode injection and kernel evidence

**The evidence supports user-mode involvement, but does not establish the complete injection mechanism or absence of all kernel assistance.** Read the [runtime report](runtime-driver-assessment.md) alongside these static findings.

## Inspected loader identity

| Form | Bytes | SHA-256 |
| --- | ---: | --- |
| Original Loader.exe | 5,438,464 | f3d3311ed76379db8bb8704aad760c728d1102325558526a9c423f67bc310e7c |
| Decompressed loader | 11,896,832 | baadd8693ecbc88c1cc71ab0256d869b6e9a6c8effb1f90708668d70c600be58 |

The loader binary itself is not included. Its import/name-check evidence is in [loader-kernel-static-indicators.json](../evidence/loader-kernel-static-indicators.json).

The original is an x64 PE32+ GUI executable with standard UPX packing and three sections. Decompression produced thirteen sections. Its manifest requests `requireAdministrator` and `uiAccess=false`. Elevation is compatible with ordinary user-mode process access and does not establish kernel execution.

## Static capabilities and limits

The decompressed image declares eighteen imported DLL descriptors and 314 imported functions. Imports include OpenProcess, ReadProcessMemory, WriteProcessMemory, VirtualAllocEx, VirtualProtectEx, CreateRemoteThread, LoadLibraryA and GetProcAddress. They support a user-mode injection hypothesis. Import presence does not prove that these functions executed, their parameters, or their sequence.

DeviceIoControl and hardware-device enumeration APIs are also imported. Those capabilities alone do not establish a cheat driver, its device endpoint, or an executed IOCTL. The [limited direct-call analysis](../evidence/loader-device-call-analysis.json) did not identify a direct DeviceIoControl IAT call; indirect wrappers and dynamic resolution were not comprehensively covered.

Selected static checks did not identify driver-loading/service-creation APIs, `.sys` filename tokens, a Nenyoo-specific kernel image, or known selected kernel-helper markers. The [marker recheck](../evidence/Nenyoo-kernel-marker-recheck.json) records its tested terms and limitations. Plain-text negatives cannot exclude transformed data, dynamically obtained helpers, an existing driver, or omitted code paths.

## Runtime outcome

The cached menu DLL appeared as a loaded image in both the loader and GTA Enhanced. No new ordinary kernel image load was identified in the retained trace. The only ordinary `.sys` unload was BEDaisy.sys following game shutdown. Approximately 3.1 seconds of loader startup were outside the retained event window.

No kernel manual mapper, driver signing/loading mechanism, vulnerable-driver use, or exact injection API call sequence was established. Neither these findings nor the static differences establish false advertising or fraud. Scooby is a separate product; its static driver indicators are not evidence about this loader.

API references: Microsoft's [VirtualAllocEx](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex), [WriteProcessMemory](https://learn.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory), [CreateRemoteThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createremotethread) and [DeviceIoControl](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-deviceiocontrol) documentation.
