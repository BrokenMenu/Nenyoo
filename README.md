# Nenyoo

**MVP Enhanced and MVP Legacy DLL analysis, focused on the reported BattlEye bypass claim.** Original GTA V menu captures, verified hashes and assessment evidence.

- **No MVP-exclusive executable content was found.** Each MVP capture contains its matching VIP file unchanged, plus ASCII-space padding: 2,334 bytes for Enhanced and 2,675 for Legacy. All nine decompressed sections match within each pair.
- **A working BattlEye bypass remains unverified.** Both MVP DLLs contain BattlEye-related text and static device-control references. Neither establishes bypass functionality; shared features may be controlled by runtime state or entitlement.
- **User-mode involvement was observed; kernel injection was not demonstrated.** The retained runtime trace missed about 3.1 seconds of loader startup. It does not establish the complete injection mechanism or the cause of reported bans.

## MVP DLLs

| Game edition | Original packed capture | Decompressed copy |
| --- | --- | --- |
| Enhanced | [MVP-Enhanced.packed.dll](MVP-Enhanced.packed.dll) | [MVP-Enhanced.unpacked.dll](artifacts/unpacked/MVP-Enhanced.unpacked.dll) |
| Legacy | [MVP-Legacy.packed.dll](MVP-Legacy.packed.dll) | [MVP-Legacy.unpacked.dll](artifacts/unpacked/MVP-Legacy.unpacked.dll) |

[VIP Enhanced](VIP-Enhanced.packed.dll) and [VIP Legacy](VIP-Legacy.packed.dll) are comparison baselines. MVP tier attribution follows the reported selection and changed cache artifact; live MVP module enumeration was unavailable. The separate runtime trace was not independently attributed to an MVP tier.

## Evidence

[Expanded MVP assessment](reports/MVP-bypass-assessment.md) · [VIP/MVP comparison](reports/variant-comparison.md) · [Runtime limits](reports/runtime-driver-assessment.md) · [Sections and protections](reports/sections-and-protections.md) · [SHA-256 manifest](evidence/artifact-manifest.json)

Verify files with `python tools/verify_artifacts.py`. Repeat the static MVP checks with `python tools/assess_mvp.py`; optional `--with-capstone` adds limited imported-call reference counts. Neither command executes the DLLs.

Account credentials, personal identifiers and raw machine-wide captures are excluded. These are assessment artifacts, not an official release; no license to third-party binaries is asserted.
