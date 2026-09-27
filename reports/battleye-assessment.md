# Nenyoo BattlEye bypass claim assessment: VIP and MVP evidence

**A working BattlEye bypass was not established by this assessment.** No separately identified bypass component or implementation is included in this repository.

The later [expanded MVP assessment](MVP-bypass-assessment.md) adds fresh PE/import parsing, all selected literal occurrences, exact padding verification and limited direct IAT-reference counts for both MVP editions. It preserves the same unverified-functionality conclusion.

This assessment examines an operator-reported MVP bypass claim. No independently archived vendor statement or feature demonstration is included. The question is what the inspected files and retained runtime observations establish, rather than assuming either success or false advertising.

## Static word matches

Offline fixed-term checks found two separate words in all four decompressed DLLs:

| Edition | BattlEye ASCII file offset | bypass ASCII file offset | VIP/MVP difference |
| --- | ---: | ---: | --- |
| Enhanced | 11,782,840 | 11,728,925 | Same offsets and file body |
| Legacy | 11,888,216 | 11,834,253 | Same offsets and file body |

Neither word was found in the decompressed loader by the selected ASCII/UTF-16 checks. BEDaisy, BEService and the alternate spelling BattleEye were not found in the five checked files. [Evidence and method](../evidence/battleye-reference-check.json).

The two word matches were not linked to the same containing string, routine or executed code path. A word can describe a message or setting. Its presence does not prove a functioning bypass; its absence would not exclude transformed code or server/loader behavior.

## Runtime observation

GTA ended before the existing BEDaisy.sys driver unloaded. A subsequent delete-path event had BEService context, followed by BEService process termination. This sequence does not establish bypass activation, the cause of game termination, or who requested the driver unload. The delete-path event alone does not prove successful file deletion. See the [runtime report](runtime-driver-assessment.md).

## VIP/MVP comparison

The captured MVP executable sections match VIP within each edition. MVP adds only trailing ASCII spaces: 2,334 for Enhanced and 2,675 for Legacy. No MVP-exclusive executable section was found in these captures. Shared functionality gated by server entitlement, configuration, loader behavior or runtime state remains possible and was not verified.

The assessment did not demonstrate anti-cheat evasion, isolate bypass code, validate protected-online behavior, or establish dishonest vendor intent. Those conclusions cannot be inferred from identical captured sections or a negative limited trace.
