# Nenyoo DLL sections, anti-tamper evidence, and menu-payload suitability

Eight files inspected: the packed and unpacked copies of VIP/MVP Enhanced and VIP/MVP Legacy. This is a detailed static assessment of available artifacts, not a guarantee that every runtime protection has been discovered.

## Findings

**Confirmed:** standard UPX packing on all four original captures. Ordinary decompression produced native x64 DLL images with nine sections. The packed contents are compressed; section entropy alone is not evidence of cryptographic encryption.

**Indicators, not demonstrated anti-tamper mechanisms:** imports for debugger detection, thread-context operations, cryptographic hashing, and memory permission changes. No specific self-checking routine, monitored byte range, integrity-check algorithm, failure reaction, or commercial virtualization protector has been established.

**Payload identity:** the evidence strongly supports these being the menu payloads used in the observed runs. VIP source paths were confirmed in GTA's module lists, with initialization messages and matching Nenyoo/engine references. Independent loading of the recovered or decompressed copies has not been validated.

**Tier comparison:** the code body is identical between VIP and MVP within each edition. The only extra MVP bytes are ASCII spaces: 2,334 for Enhanced and 2,675 for Legacy. Their operational purpose is unverified; they do not contain distinct executable code or an encoded configuration in these captured tails.

## What counts as anti-tamper here

Anti-tamper means detecting or resisting modifications to the program, its code/data, or its execution environment. Packing can obstruct immediate inspection; anti-debug checks may change behavior during analysis; integrity checks may detect modified contents. None follows automatically from a section's name or permissions. ASLR, NX/DEP, and stack cookies are separate exploit mitigations; they are documented below as context rather than claimed custom anti-tamper systems.

## Packing and section layout

All packed files have UPX0, UPX1, and .rsrc. UPX0 has zero raw bytes but reserves a large virtual region. UPX1 has near-maximum entropy: 7.99989 bits/byte for Enhanced and 7.99988 for Legacy. Standard UPX integrity tests and decompression succeeded earlier, providing stronger packing attribution than section names or entropy alone. UPX is an executable compressor; see the [official UPX project](https://github.com/upx/upx).

The packed headers mark UPX0 and UPX1 RWX. That is consistent with unpacking code/data into memory. It does not prove how permissions behave after initialization. After standard decompression, .text is R-X; .data and .tls are RW-; other sections are R--. There is no section simultaneously marked writable and executable in the decompressed headers. These are on-disk declarations, not a measurement of live game-page permissions.

R means readable, W writable, X executable, and a dash means that flag is absent. Entropy is Shannon entropy over raw file bytes, on a 0–8 scale; empty raw sections have no entropy measurement. Table interpretations use Microsoft's [PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format).

### Enhanced, packed

| Section | RVA | File offset | File bytes | Virtual bytes | Permissions | Entropy | Contents |
| --- | --- | --- | ---: | ---: | --- | ---: | --- |
| UPX0 | 0x1000 | 0x400 | 0 | 16,289,792 | RWX | N/A | Virtual destination for expanded contents; no raw bytes in this file. |
| UPX1 | 0xF8A000 | 0x400 | 2,938,880 | 2,940,928 | RWX | 8.000 | Compressed executable contents and unpacking-related code. |
| .rsrc | 0x1258000 | 0x2CDC00 | 3,072 | 4,096 | RW- | 4.371 | PE resources; packed layout also contains preserved loader metadata. |

### Enhanced, unpacked

| Section | RVA | File offset | File bytes | Virtual bytes | Permissions | Entropy | Contents |
| --- | --- | --- | ---: | ---: | --- | ---: | --- |
| .text | 0x1000 | 0x400 | 10,811,392 | 10,811,291 | R-X | 5.490 | Native machine code. |
| .rdata | 0xA51000 | 0xA4FC00 | 3,471,872 | 3,471,696 | R-- | 5.133 | Constants, read-only structures, and readable strings. |
| .data | 0xDA1000 | 0xD9F600 | 2,717,696 | 4,276,641 | RW- | 2.733 | Mutable globals and initialized state; virtual size also reserves non-file-backed data. |
| .pdata | 0x11B6000 | 0x1036E00 | 420,864 | 420,756 | R-- | 6.128 | x64 exception/unwind-related records. |
| .idata | 0x121D000 | 0x109DA00 | 38,400 | 37,903 | R-- | 4.104 | Windows DLL/function import metadata. |
| .tls | 0x1227000 | 0x10A7000 | 1,024 | 852 | RW- | 0.011 | Thread-local storage. |
| .00cfg | 0x1228000 | 0x10A7400 | 512 | 373 | R-- | 0.427 | Compiler-generated control-flow support/configuration slots. |
| .rsrc | 0x1229000 | 0x10A7600 | 1,536 | 1,084 | R-- | 2.149 | PE resources; packed layout also contains preserved loader metadata. |
| .reloc | 0x122A000 | 0x10A7C00 | 125,440 | 124,986 | R-- | 4.010 | Base relocation records. |

### Legacy, packed

| Section | RVA | File offset | File bytes | Virtual bytes | Permissions | Entropy | Contents |
| --- | --- | --- | ---: | ---: | --- | ---: | --- |
| UPX0 | 0x1000 | 0x400 | 0 | 16,392,192 | RWX | N/A | Virtual destination for expanded contents; no raw bytes in this file. |
| UPX1 | 0xFA3000 | 0x400 | 2,956,800 | 2,957,312 | RWX | 8.000 | Compressed executable contents and unpacking-related code. |
| .rsrc | 0x1275000 | 0x2D2200 | 3,072 | 4,096 | RW- | 4.326 | PE resources; packed layout also contains preserved loader metadata. |

### Legacy, unpacked

| Section | RVA | File offset | File bytes | Virtual bytes | Permissions | Entropy | Contents |
| --- | --- | --- | ---: | ---: | --- | ---: | --- |
| .text | 0x1000 | 0x400 | 10,909,696 | 10,909,616 | R-X | 5.492 | Native machine code. |
| .rdata | 0xA69000 | 0xA67C00 | 3,486,720 | 3,486,656 | R-- | 5.145 | Constants, read-only structures, and readable strings. |
| .data | 0xDBD000 | 0xDBB000 | 2,718,208 | 4,276,833 | RW- | 2.734 | Mutable globals and initialized state; virtual size also reserves non-file-backed data. |
| .pdata | 0x11D2000 | 0x1052A00 | 423,936 | 423,600 | R-- | 6.129 | x64 exception/unwind-related records. |
| .idata | 0x123A000 | 0x10BA200 | 37,888 | 37,810 | R-- | 4.184 | Windows DLL/function import metadata. |
| .tls | 0x1244000 | 0x10C3600 | 1,024 | 861 | RW- | 0.011 | Thread-local storage. |
| .00cfg | 0x1245000 | 0x10C3A00 | 512 | 373 | R-- | 0.432 | Compiler-generated control-flow support/configuration slots. |
| .rsrc | 0x1246000 | 0x10C3C00 | 1,536 | 1,084 | R-- | 2.147 | PE resources; packed layout also contains preserved loader metadata. |
| .reloc | 0x1247000 | 0x10C4200 | 125,440 | 125,424 | R-- | 4.016 | Base relocation records. |


The tables describe VIP and MVP equally within an edition because their headers and section bytes are identical. Precise hashes, flag values, directory addresses, and each file's duplicated inventory are in ../evidence/dll-protection-evidence.json. The relocation sections are marked discardable; other sections are not.

## Is a section specifically protected or encrypted?

The confirmed packed region is UPX1, together with UPX0 as the expansion destination. These are a packing arrangement, not evidence of authenticated tamper checking. No dedicated virtual-machine or commercial-protector section was identified after decompression.

Unpacked .text entropy is 5.48998 for Enhanced and 5.49207 for Legacy. Read-only data entropy is 5.1333 and 5.1449. Those whole-section measurements do not support labeling the entire unpacked section as encrypted; small encrypted/obfuscated regions could still exist. No encryption algorithm, key, virtualized instruction set, or protected function boundary has been attributed.

Fixed ASCII/UTF-16 checks found no matches for VMProtect, Themida, WinLicense, Enigma Protector, Obsidium, Code Virtualizer. This is not a complete protector-signature database or proof of absence. Marker stripping, custom protection, dynamic resolution, or transformed components can evade such checks. Obfuscation and virtualization cannot be excluded merely because ordinary section names are present.

## Anti-debug and analysis-related evidence

| Name | Imported in Enhanced | Imported in Legacy | Literal/sub-string present |
| --- | --- | --- | --- |
| IsDebuggerPresent | Yes | Yes | Enhanced: yes; Legacy: yes |
| CheckRemoteDebuggerPresent | No | No | Enhanced: no; Legacy: no |
| NtQueryInformationProcess | No | No | Enhanced: no; Legacy: no |
| NtSetInformationThread | No | No | Enhanced: no; Legacy: no |
| OutputDebugStringA | Yes | Yes | Enhanced: yes; Legacy: yes |
| DebugActiveProcess | No | No | Enhanced: yes; Legacy: yes |
| DebugBreak | No | No | Enhanced: yes; Legacy: yes |
| GetThreadContext | Yes | Yes | Enhanced: yes; Legacy: yes |
| SetThreadContext | Yes | Yes | Enhanced: yes; Legacy: yes |

IsDebuggerPresent provides debugger detection capability, as described by [Microsoft](https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-isdebuggerpresent). It can also be called by ordinary runtime error handling. OutputDebugStringA is a diagnostic API. GetThreadContext and SetThreadContext can support exceptions, debugging, or other thread work. Their imports do not establish active debugger rejection, hardware-breakpoint detection, or tamper response. Literal matches that are not exact imports may be substrings of longer identifiers; they were not interpreted as confirmed calls.

No selected plain-text debugger-rejection messages were found. No debugger was attached, checks were patched, threads suspended, or anti-debug behavior exercised. Timing checks, PEB inspection, exception tricks, indirect API resolution, and custom checks remain unverified rather than declared absent.

## Hashing, signatures, and self-integrity

Both distinct DLL bodies import CryptCreateHash, CryptHashData, CryptGetHashParam, and CryptQueryObject. These can support hashing or certificate-related operations, but can also belong to unrelated cryptographic/library code. This assessment does not establish that the DLL hashes its own .text, validates imports, checks hooks, authenticates an on-disk file, or periodically verifies runtime pages.

The searched WinVerifyTrust and RtlComputeCrc32 names were not found as imports or plain-text matches. Custom/inlined checks may not use those names. No custom checksum loop or its protected range was verified. Standard UPX integrity-test success establishes consistency of the packed file; it is not proof of an application-level tamper policy.

All eight files have zero bytes in their embedded PE certificate directory, and FORCE_INTEGRITY is unset. No embedded Authenticode certificate was found by the header check. Catalog trust and application-level signature verification were not evaluated. Neither observation proves the absence of custom integrity checking.

## Compiler and operating-system metadata

These results are common to all captures, apart from addresses belonging to their respective edition. They are not commercial anti-tamper attribution.

| Item | Enhanced | Legacy | What is established |
| --- | --- | --- | --- |
| DLL characteristics | 0x160 | 0x160 | Header flags only |
| DYNAMIC_BASE / relocations | Set / present | Set / present | Relocation capability declared |
| HIGH_ENTROPY_VA | Set | Set | 64-bit high-entropy address capability declared |
| NX_COMPAT | Set | Set | NX compatibility declared |
| Security-cookie VA | 0x180F7FE00 | 0x180F9BD40 | Nonzero load-config cookie pointer, file-backed after unpacking |
| Load-config size | 320 bytes | 320 bytes | Parsed structure |
| GuardFlags | 0x100 | 0x100 | CF_INSTRUMENTED metadata bit set |
| GUARD_CF optional-header flag | Unset | Unset | Image does not advertise this header flag |
| CFG target table / count | Zero / 0 | Zero / 0 | No declared target table |
| Guard EH continuation table / count | Zero / 0 | Zero / 0 | No declared continuation table |
| Guard XFG pointer fields | Nonzero | Nonzero | Support slots present; enforcement not proven |
| CET debug characteristics | No such record found | No such record found | No explicit CET compatibility metadata located |

The nonzero security-cookie pointer is evidence of stack-cookie support metadata. It is not a count of protected functions, and does not establish that every function uses /GS. Microsoft's [/GS description](https://learn.microsoft.com/en-us/cpp/build/reference/gs-buffer-security-check) distinguishes stack-buffer checks from other protections.

Control-flow metadata is mixed: the load configuration advertises instrumentation, but the optional-header GUARD_CF flag is unset and the target table/count are zero. Nonzero CF/XFG pointer slots alone are insufficient to claim complete or active CFG/XFG enforcement. No runtime enforcement test was performed. See [Microsoft load configuration](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-image_load_config_directory64) and [CFG compiler documentation](https://learn.microsoft.com/en-us/cpp/build/reference/guard-enable-control-flow-guard). CET compatibility would be recorded separately; see [Microsoft CETCOMPAT](https://learn.microsoft.com/en-us/cpp/build/reference/cetcompat).

The packed cookie pointers target regions with no corresponding on-disk expanded bytes, so the parser reports that packed backing check as unavailable. The unpacked cookies are file-backed. This is expected coverage behavior for compressed images, not evidence of missing cookies or corruption. All other parsed unpacked protection fields produced no warnings.

## TLS, exception handling, symbols, and resources

Both editions have thread-local storage directories. The unpacked callback-array pointers are nonzero but the first callback entry is zero: no TLS callbacks were enumerated. The packed callback pointers are zero. This provides no evidence of an anti-tamper TLS callback; checks could still execute through other initialization code.

The Enhanced exception directory declares 31,853 twelve-byte runtime-function records; Legacy declares 32,069. These counts refer to directory entries, not identified source functions or anti-tamper routines. .pdata includes exception/unwind-related data; it is not automatically a protected section. SafeSEH's x86 handler-table interpretation is not applicable to these x64 images.

No debug-directory entries or COFF symbol-table entries were found. That limits available symbol information but does not establish deliberate symbol stripping as an anti-tamper mechanism. PE sections and compiler metadata are still readable.

Each unpacked edition has one resource leaf: RT_MANIFEST (type 24), resource ID 2, language 1033, 381 bytes. The manifest requests asInvoker with uiAccess=false. It does not elevate the host game through the DLL. No icon, version, or bitmap leaf was present in this PE resource tree; other assets can live in ordinary data sections or external files. The packed .rsrc layout also preserves PE loading metadata, so its section size exceeds that manifest alone.

## MVP trailing bytes: additional finding

| File family | Extra bytes versus VIP | Values | Interpretation |
| --- | ---: | --- | --- |
| MVP Enhanced, packed and unpacked | 2,334 | Every byte is 0x20 | Repeated ASCII-space padding |
| MVP Legacy, packed and unpacked | 2,675 | Every byte is 0x20 | Repeated ASCII-space padding |

These tails have entropy 0. They are not a separate executable section, nontrivial encrypted blob, or tier configuration encoded in varied byte contents. A program could still observe file length or padding length, so its operational use remains unverified. Earlier reports called this unexplained appended data; the byte values are now known. Tier differences could depend on runtime state, the loader, or server decisions, but none of those explanations was established.

## Are these the actual game-menu DLLs?

**The evidence strongly supports that attribution for the observed runs.**

| Evidence | Enhanced | Legacy | Limit |
| --- | --- | --- | --- |
| Native x64 PE DLL | Confirmed | Confirmed | Format validity alone does not prove identity |
| Actual VIP game's module list points to source cache | Confirmed | Confirmed | Captured in earlier VIP runs |
| Nenyoo / Engine Loaded! / legacyv2 references | Present | Present | References alone are insufficient |
| ImGui and Lua references | Present | Present | Support UI/scripting attribution, not a feature inventory |
| D3DCOMPILER_47, USER32, input/runtime/network imports | Present | Present | Available capabilities, not traced use |
| Vendor-run initialization observed | Enhanced engine/renderer messages recorded | Loaded source confirmed | Earlier observations, not a new independent execution test |
| MVP body matches the edition's VIP body | Confirmed | Confirmed | MVP live module enumeration was unavailable |

All four expose one named export, D3DReflectLibrary. An export name by itself is not proof of the module's overall purpose. The combined game module, cache timing, native payload format, and menu identity evidence is stronger. Linker version metadata is 14.44; C++ runtime imports and no CLR directory support a native C/C++ build interpretation, rather than a managed .NET assembly.

The files are injectable menu payloads based on observed use. They are not identified as replacements for GTA's executable or a particular shipped game DLL. Enhanced and Legacy code bodies differ, so the edition labels should be retained. Header inspection cannot certify compatibility with every game update or initialization environment. No stand-alone host, independently injected recovered file, or feature-by-feature menu test was executed. UPX-decompressed copies are analysis artifacts; their headers may be reconstructed by UPX, and successful normal loading of the original cache does not certify identical behavior of those reconstructed files.

## Coverage, reproducibility, and remaining questions

The inspection read local files only. The loader was not launched or logged into, Nenyoo endpoints were not contacted, binaries were not modified, and no anti-tamper or anti-cheat protection was disabled. All eight fresh file hashes still matched the recovery manifest.

The script parses file-backed section ranges, import names, PE directories, load configuration, TLS arrays, export names, resource leaves, and debug metadata; it measures raw-byte entropy and selected literal references. Its detailed results are in ../evidence/dll-protection-evidence.json and the reproduction script inspect-dll-protections.mjs. Every section's metadata was checked against the earlier independent header inspector; artifact sizes/hashes were checked against the established manifest.

Unknowns include custom code-page hashing, runtime memory transformations, selected function obfuscation/virtualization, dynamic debugger checks, self-repair or tamper responses, server-side licensing, and the complete feature set. These require call-path analysis or appropriately scoped runtime evidence; static imports and section names cannot answer them completely. No working BattlEye bypass or kernel protection layer has been established by this report.

## Evidence index

- ../evidence/dll-protection-evidence.json: all eight artifact inventories, hashes, section flags/entropy, imports, mitigation metadata, callbacks, debug entries, resource leaves, and fixed-name checks.
- inspect-dll-protections.mjs: static inspection script.
- dll-protection-analysis-output.json: captured selected inspection output.
- ../evidence/All-variants-comparison.json and .md: complete pairwise body/section comparisons.
- recovered/hash-manifest.json: original recovery hashes.
- recovered/Recovery-report.md and per-variant recovery records: provenance, normal module observations, and attribution limits.
- Nenyoo-loader-kernel-assessment.md: related loader/driver/event evidence.
- battleye-reference-check.json: reference checks, distinct from a bypass implementation finding.

Publication note: this is a copy of the local static report with workstation paths redacted. The repository includes the captured originals and separately decompressed derivatives. Historical raw machine-wide observations and credentials are not included.
