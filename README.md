# Nenyoo

**Nenyoo GTA V menu DLL analysis:** original VIP and MVP captures for Enhanced and Legacy, with file comparisons, BattlEye bypass claim assessment, and injection observations. This repository tests reported menu claims against preserved artifacts and explains what the evidence can establish.

The four original packed DLLs are available directly in the repository root. Separately decompressed copies remain in [`artifacts/unpacked`](artifacts/unpacked). These are assessment captures, not an official source release; independent execution of the copies has not been validated.

## Nenyoo VIP vs MVP: confirmed DLL differences

Within each game edition, **the captured MVP file contains the corresponding VIP file unchanged, followed only by ASCII-space padding**. This holds for both original packed captures and decompressed derivatives.

| Comparison | Matching decompressed sections | Additional MVP bytes | Additional content |
| --- | ---: | ---: | --- |
| VIP Enhanced vs MVP Enhanced | 9 of 9 | 2,334 | ASCII spaces (`0x20`) |
| VIP Legacy vs MVP Legacy | 9 of 9 | 2,675 | ASCII spaces (`0x20`) |

Enhanced and Legacy have different DLL bodies. Matching VIP/MVP sections establish file contents, not identical runtime features, account entitlements, configuration or server behavior. See the [full Nenyoo VIP/MVP comparison](reports/variant-comparison.md) and [section/hash evidence](evidence/All-variants-comparison.json).

## Nenyoo BattlEye bypass claim: evidence and limits

**A working BattlEye bypass was not verified.** The MVP bypass claim was reported by the operator; an independently archived vendor promise or feature demonstration is not included in this repository.

Separate occurrences of the words `BattlEye` and `bypass` were found in all four decompressed DLLs. These word matches do not establish an executed bypass or its mechanism. No MVP-exclusive executable section was found in the captures. Shared functionality controlled by runtime state or account entitlement remains possible and was not verified. See the [BattlEye claim assessment](reports/battleye-assessment.md).

## Nenyoo injection observations: user mode and kernel evidence

**User-mode involvement was observed; kernel-level injection was not demonstrated.** The cached DLL loaded into the loader and GTA. No new conventional kernel image load appeared in the retained runtime events. The driver unload was BattlEye's existing BEDaisy.sys after GTA ended; the cause of shutdown was not established.

Approximately **3.1 seconds of loader startup were missing** from the circular trace. A temporary driver in that gap, assistance from an existing driver, or an unobserved mechanism cannot be excluded. User-mode module loading does not establish the entire injection route or decide whether a reported bypass works. See the [loader assessment](reports/loader-and-kernel-assessment.md) and [runtime timeline and coverage limits](reports/runtime-driver-assessment.md).

## Packing and anti-tamper indicators

**Standard UPX packing was confirmed.** Decompressed DLLs have nine sections. Debugger-detection and other protection-related imports are indicators; a specific custom anti-tamper implementation was not demonstrated. The [sections and protections report](reports/sections-and-protections.md) distinguishes observed packing, import capabilities and unverified runtime behavior.

These observations do not establish fraud, prove every advertised capability absent, or certify that kernel assistance is impossible.

## Original Nenyoo DLL captures: Enhanced and Legacy

| Selection | Original packed DLL | Bytes | Decompressed derivative |
| --- | --- | ---: | --- |
| VIP Enhanced | [VIP-Enhanced.packed.dll](VIP-Enhanced.packed.dll) | 2,942,976 | [VIP-Enhanced.unpacked.dll](artifacts/unpacked/VIP-Enhanced.unpacked.dll) |
| MVP Enhanced | [MVP-Enhanced.packed.dll](MVP-Enhanced.packed.dll) | 2,945,310 | [MVP-Enhanced.unpacked.dll](artifacts/unpacked/MVP-Enhanced.unpacked.dll) |
| VIP Legacy | [VIP-Legacy.packed.dll](VIP-Legacy.packed.dll) | 2,960,896 | [VIP-Legacy.unpacked.dll](artifacts/unpacked/VIP-Legacy.unpacked.dll) |
| MVP Legacy | [MVP-Legacy.packed.dll](MVP-Legacy.packed.dll) | 2,963,571 | [MVP-Legacy.unpacked.dll](artifacts/unpacked/MVP-Legacy.unpacked.dll) |

Tier labels follow operator-reported selections. VIP source paths were confirmed in conventional loaded-module lists. Live module enumeration was unavailable for the MVP runs; attribution used the reported selection, changed cache artifact and running game edition. The later runtime capture is not independently labeled VIP or MVP.

## Analysis reports and reproducible evidence

- [VIP/MVP and Enhanced/Legacy comparison](reports/variant-comparison.md)
- [Sections, packing and anti-tamper indicators](reports/sections-and-protections.md)
- [Loader and kernel assessment](reports/loader-and-kernel-assessment.md)
- [Runtime driver observations and coverage gap](reports/runtime-driver-assessment.md)
- [BattlEye findings and limits](reports/battleye-assessment.md)
- [SHA-256 artifact manifest](evidence/artifact-manifest.json)

Run `python tools/verify_artifacts.py` from the repository root to check all eight files against the manifest and independently repeat the VIP/MVP prefix and padding comparisons. The verifier reads files and does not execute any DLL.

Published evidence excludes account credentials, personal identifiers, workstation paths, raw machine-wide captures and account configuration. Target process IDs and absolute runtime timestamps have been replaced with roles and relative times. The binary artifacts retain their captured hashes; they are not modified or patched for publication.

No license to third-party binary code is asserted by this repository.
