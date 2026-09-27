# Nenyoo VIP vs MVP DLL comparison: GTA V Enhanced and Legacy


All four selected variants have preserved packed and unpacked files. There are two distinct DLL bodies in these captures: Enhanced and Legacy. Within each edition, VIP and MVP have identical headers and all nine unpacked sections. MVP Enhanced adds 2,334 trailing bytes; MVP Legacy adds 2,675 trailing bytes. None of the complete files are byte-identical, because of either appended data or different DLL bodies.

| Variant | Packed bytes | Unpacked bytes | Unpacked body bytes | Trailing bytes |
| --- | ---: | ---: | ---: | ---: |
| VIP-Enhanced | 2,942,976 | 17,589,760 | 17,589,760 | 0 |
| MVP-Enhanced | 2,945,310 | 17,592,094 | 17,589,760 | 2,334 |
| VIP-Legacy | 2,960,896 | 17,705,984 | 17,705,984 | 0 |
| MVP-Legacy | 2,963,571 | 17,708,659 | 17,705,984 | 2,675 |

| Pair | Headers identical | DLL body identical | Matching unpacked sections | Complete file identical |
| --- | --- | --- | ---: | --- |
| VIP-Enhanced / MVP-Enhanced | Yes | Yes | 9/9 | No |
| VIP-Enhanced / VIP-Legacy | No | No | 0/9 | No |
| VIP-Enhanced / MVP-Legacy | No | No | 0/9 | No |
| MVP-Enhanced / VIP-Legacy | No | No | 0/9 | No |
| MVP-Enhanced / MVP-Legacy | No | No | 0/9 | No |
| VIP-Legacy / MVP-Legacy | Yes | Yes | 9/9 | No |

Each MVP capture contains the complete corresponding VIP file unchanged, followed by the additional trailing data. This holds for both packed and unpacked files. Enhanced versus Legacy differs in code, data, imports, resources, and the other sections; all nine unpacked sections differ.

These results establish file contents, not identical runtime features or permissions. The appended data's purpose remains unverified, and server-side behavior was not examined. No Windows filesystem journal was inspected.

Variant labels follow the user's selected-tier reports. VIP Enhanced and VIP Legacy source paths were confirmed in their game's conventional loaded-module lists. Module enumeration was unavailable for both MVP captures; attribution also uses the corresponding changed cache file and running game edition. All copies were checked against source hashes and passed standard UPX integrity testing and decompression.

Detailed section hashes and all twelve comparisons (six pairs in each form): ../evidence/All-variants-comparison.json. Whole-file hashes: ../evidence/artifact-manifest.json.

Later inspection established that every appended MVP byte is ASCII space (0x20). This does not establish how tier permissions or features are implemented.
