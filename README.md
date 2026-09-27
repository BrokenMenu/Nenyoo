# Nenyoo

Captured **GTA V mod-menu DLLs** associated with Nenyoo VIP and MVP on Enhanced and Legacy, with static comparisons and a limited runtime driver assessment. These are preserved assessment artifacts, not an official source release. Independent execution of the copied or decompressed DLLs has not been validated.

## Findings

- **User-mode involvement was observed. Kernel-level injection was not demonstrated.** The cached DLL loaded into the loader and GTA. No new conventional kernel image load appeared in the retained runtime events. Approximately the first 3.1 seconds of loader startup were missing from the circular trace, and assistance from an existing driver remains possible.
- **A working BattlEye bypass was not verified.** Separate occurrences of the words `BattlEye` and `bypass` were found in all four decompressed DLLs. They do not establish an executed bypass or a mechanism. The runtime driver unload was the existing BattlEye driver after GTA ended; its cause and relationship to menu behavior were not established.
- **Within each edition, the captured MVP file contains the corresponding VIP file unchanged, followed by ASCII-space padding.** Enhanced adds 2,334 bytes; Legacy adds 2,675. All nine decompressed sections match within each pair. This establishes captured file contents, not identical runtime features, entitlement checks, or server behavior.
- **Standard UPX packing was confirmed.** Decompressed DLLs have nine sections. Debugger-detection and other protection-related imports are indicators; a specific custom anti-tamper implementation was not demonstrated.

These observations do not establish fraud, prove every advertised capability absent, or certify that kernel assistance is impossible.

## DLL captures

| Selection | Original packed DLL | Bytes | Decompressed derivative |
| --- | --- | ---: | --- |
| VIP Enhanced | [VIP-Enhanced.packed.dll](artifacts/original/VIP-Enhanced.packed.dll) | 2,942,976 | [VIP-Enhanced.unpacked.dll](artifacts/unpacked/VIP-Enhanced.unpacked.dll) |
| MVP Enhanced | [MVP-Enhanced.packed.dll](artifacts/original/MVP-Enhanced.packed.dll) | 2,945,310 | [MVP-Enhanced.unpacked.dll](artifacts/unpacked/MVP-Enhanced.unpacked.dll) |
| VIP Legacy | [VIP-Legacy.packed.dll](artifacts/original/VIP-Legacy.packed.dll) | 2,960,896 | [VIP-Legacy.unpacked.dll](artifacts/unpacked/VIP-Legacy.unpacked.dll) |
| MVP Legacy | [MVP-Legacy.packed.dll](artifacts/original/MVP-Legacy.packed.dll) | 2,963,571 | [MVP-Legacy.unpacked.dll](artifacts/unpacked/MVP-Legacy.unpacked.dll) |

Tier labels follow operator-reported selections. VIP source paths were confirmed in conventional loaded-module lists. Live module enumeration was unavailable for the MVP runs; attribution used the reported selection, changed cache artifact and running game edition. The later runtime capture is not independently labeled VIP or MVP.

## Reports and evidence

- [VIP/MVP and Enhanced/Legacy comparison](reports/variant-comparison.md)
- [Sections, packing and anti-tamper indicators](reports/sections-and-protections.md)
- [Loader and kernel assessment](reports/loader-and-kernel-assessment.md)
- [Runtime driver observations and coverage gap](reports/runtime-driver-assessment.md)
- [BattlEye findings and limits](reports/battleye-assessment.md)
- [SHA-256 artifact manifest](evidence/artifact-manifest.json)

Run `python tools/verify_artifacts.py` from the repository root to check all eight files against the manifest and independently repeat the VIP/MVP prefix and padding comparisons. The verifier reads files and does not execute any DLL.

Published evidence excludes account credentials, personal identifiers, workstation paths, raw machine-wide captures and account configuration. Target process IDs and absolute runtime timestamps have been replaced with roles and relative times. The binary artifacts retain their captured hashes; they are not modified or patched for publication.

No license to third-party binary code is asserted by this repository.
