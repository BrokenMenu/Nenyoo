# Nenyoo runtime injection assessment: driver events and coverage limits

Recording has stopped. This is a follow-up to [the static loader assessment](loader-and-kernel-assessment.md). This publication copy uses process roles and relative times rather than machine identifiers and absolute timestamps.

## Result

**This recording did not demonstrate a Nenyoo kernel injector or kernel manual mapper.** It recorded the cached menu DLL loading into both Loader.exe and GTA5_Enhanced.exe. No ordinary new kernel image load appeared in the retained trace. The driver unload that appeared was BEDaisy.sys, the existing BattlEye driver, after the GTA process ended.

**The negative driver result is incomplete:** this run used circular memory buffers. The earliest retained ordinary file/registry activity is roughly 3.1 seconds after the loader's sampled start time. A short-lived driver at loader startup could have fallen outside the retained window. This run therefore cannot rule out that possibility.

## What was recorded

Windows Performance Recorder collected ProcessThread, Loader, FileIO, FileIOInit and Registry events. The profile used 2,048 buffers of 64 KB in memory mode. A separate elevated recorder sampled conventional driver and service metadata and target process metadata. It completed 24 samples with zero reported sampler errors. There were 441 conventional driver entries before and 440 after; service inventories contained 306 entries at both endpoints. These are inventory entries, not counts of simultaneously loaded kernel modules.

The recorder started before Loader.exe opened. At baseline, GTA5_Enhanced.exe and BEService.exe were already running. The operator launched the loader and performed the normal injection. This assessment did not log into the loader, hook it, dump process memory, extract another payload, or change security settings. It did not capture request bodies or identify a download URL.

The saved ETL is 146,407,424 bytes. Windows tracerpt processed 1,117 buffers and 1,574,654 events, reporting zero lost events. The CSV analysis parsed 1,574,653 data rows. Zero reported event loss does not establish preservation of the start of a circular recording.

## Timeline

Times below are seconds relative to the cached DLL loading into GTA (zero). The cache artifact is labeled `cached-menu.dll`; its workstation path and cache identifier are omitted. No VIP/MVP tier is inferred from this run.

| Relative seconds | Observation | Meaning |
| --- | --- | --- |
| -51.855 | Recorder start | Session began before loader launch. |
| -18.596 | Loader start time, reported by process sampling | The corresponding ordinary ETW launch event was not retained. |
| -15.507 | Earliest retained ordinary file/registry activity | Approximately 3.1 seconds of loader startup are outside the retained activity window. |
| -0.499 | Loader file open/create activity for the cached DLL | Establishes access; the event alone does not establish creation of a new file. |
| -0.400 | Image Load for the cached DLL in loader context | The module loaded into the loader. |
| 0.000 | Image Load for the same cached DLL in game context | The module loaded into GTA Enhanced. |
| +4.524 | Loader.exe process End | Loader exited after the module load. |
| +17.410 | GTA5_Enhanced.exe process End | The game process ended. The trace does not establish why. |
| +17.626 | GTA5_Enhanced_BE.exe process End | The associated launcher process ended. |
| +19.224 | BEDaisy.sys Image UnLoad in kernel context | Existing BattlEye kernel driver unloaded after the game ended. |
| +19.225 | BEDaisy.sys FileIo DletePath in BEService context | Successful deletion is not established by this event alone. |
| +19.254 | BEService.exe process End | BattlEye service process ended. |
| +20.366 | Sampler detected BEDaisy service entry removal and BEService stopped | Consistent with the shutdown sequence; not evidence of a Nenyoo-specific driver. |
| +30.157 | Final stopped status saved | WPR trace saved and this recorder stopped. |

## Driver and registry interpretation

The retained Image Load events were filtered for image PID 0 or a `.sys` path. **None matched.** BEDaisy.sys was the only ordinary `.sys` Image UnLoad identified. Its recorded path was `C:\Program Files (x86)\Common Files\BattlEye\BEDaisy.sys`.

Many existing driver images appeared in Image DCEnd records. These are rundown inventory records, not evidence that each driver newly loaded during injection. Image-event attribution used the payload image PID; the event header PID was kept separately. A header PID alone does not identify who requested a driver unload.

No `.sys` path was found in the selected named file events attributed to the loader. This does not cover unnamed operations, dynamically transformed data, or the missing startup window. The selected service-registry candidates were KCBCreate/KCBDelete bookkeeping for BEDaisy. Those event names do not demonstrate creation or deletion of a driver service registry key. The selected Service Control Manager export was empty; that absence is not proof that no service action occurred.

## What this establishes and what remains unknown

The module-loading outcome confirms user-mode involvement: the cached DLL became a conventional loaded image in the loader and GTA. It does not establish an executed OpenProcess/WriteProcessMemory/CreateRemoteThread call sequence, prove that all injection work was user-mode, or exclude assistance from an existing driver.

The prior static review found user-mode injection-related imports in Nenyoo's loader and no identified Nenyoo driver payload. Those static findings and this runtime observation agree, but neither certifies absence of kernel assistance. DeviceIoControl capability by itself is not evidence of a kernel injector. Scooby's separate static findings are not evidence about Nenyoo.

The recording did not establish kernel manual mapping, a vulnerable-driver mechanism, an anti-cheat bypass, or the cause of the game shutdown. It also did not identify the server location from which the DLL was downloaded.

## Published evidence and provenance

The [selected event export](../evidence/Nenyoo-kernel-runtime-selected-evidence.json) contains relevant target events and coverage information. Workstation paths are redacted. Raw ETL, machine-wide CSV, before/after inventories, and credentials are not published. ETL SHA-256: `394805cbf0b88eeeda4e283832cb042132d254b6f34f543b007d7a5accc00745`.

Sysmon was downloaded after this run but was not installed and contributed no events. A stronger follow-up would preserve startup with file-mode WPR, optionally corroborated by Sysmon DriverLoad events after taking a fresh baseline. Installing Sysmon adds its own service/driver.

References: [Microsoft WPR keywords](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/keyword--in-systemprovider-), [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon), [Microsoft TraceEvent kernel schema](https://github.com/microsoft/perfview/blob/main/src/TraceEvent/Parsers/kerneltraceeventparser.man.xml).
