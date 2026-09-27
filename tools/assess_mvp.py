"""Read-only MVP PE/import assessment; never loads or modifies a DLL."""
import hashlib
import json
import argparse
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
    'driverLoading': ['NtLoadDriver', 'ZwLoadDriver', 'NtUnloadDriver', 'ZwUnloadDriver'],
    'serviceControl': ['CreateServiceA', 'CreateServiceW', 'StartServiceA', 'StartServiceW', 'OpenSCManagerA', 'OpenSCManagerW', 'OpenServiceA', 'OpenServiceW', 'ControlService', 'DeleteService'],
    'deviceCommunication': ['DeviceIoControl', 'NtDeviceIoControlFile', 'ZwDeviceIoControlFile'],
    'processMemoryAndThreads': ['OpenProcess', 'ReadProcessMemory', 'WriteProcessMemory', 'VirtualAllocEx', 'VirtualProtectEx', 'CreateRemoteThread', 'NtOpenProcess', 'NtReadVirtualMemory', 'NtWriteVirtualMemory', 'NtCreateThreadEx'],
    'dynamicResolution': ['LoadLibraryA', 'LoadLibraryW', 'LoadLibraryExA', 'LoadLibraryExW', 'GetProcAddress', 'LdrGetProcedureAddress'],
}
TERMS = ['BattlEye', 'BattleEye', 'BEDaisy', 'BEService', 'bypass']

class PE:
    def __init__(self, data):
        self.data = data
        assert data[:2] == b'MZ'
        self.pe = self.u32(0x3c)
        assert data[self.pe:self.pe+4] == b'PE\0\0'
        self.optional = self.pe + 24
        assert self.u16(self.optional) == 0x20b, 'Expected PE32+'
        self.iat = {}
        self.sections = []
        table = self.optional + self.u16(self.pe + 20)
        count = self.u16(self.pe + 6)
        assert 0 < count <= 96
        for i in range(count):
            at = table + i*40
            name = self.slice(at, 8).split(b'\0')[0].decode('ascii')
            size, offset = self.u32(at+16), self.u32(at+20)
            contents = self.slice(offset, size)
            self.sections.append({'name': name, 'rva': self.u32(at+12), 'offset': offset, 'bytes': size, 'characteristics': self.u32(at+36), 'sha256': hashlib.sha256(contents).hexdigest()})

    def slice(self, offset, size):
        assert offset >= 0 and size >= 0 and offset+size <= len(self.data), 'File bounds'
        return self.data[offset:offset+size]

    def u16(self, at): return struct.unpack('<H', self.slice(at, 2))[0]
    def u32(self, at): return struct.unpack('<I', self.slice(at, 4))[0]
    def u64(self, at): return struct.unpack('<Q', self.slice(at, 8))[0]

    def offset(self, rva, size=1):
        if rva+size <= self.u32(self.optional+60):
            self.slice(rva, size)
            return rva
        for section in self.sections:
            if section['rva'] <= rva and rva+size <= section['rva']+section['bytes']:
                at = section['offset']+rva-section['rva']
                self.slice(at, size)
                return at
        raise ValueError('RVA is not file-backed')

    def string(self, rva):
        at = self.offset(rva)
        end = self.data.find(b'\0', at, min(at+2048, len(self.data)))
        assert end >= 0, 'String bounds'
        self.offset(rva, end-at+1)
        return self.data[at:end].decode('ascii')

    def directory(self, index):
        if index >= self.u32(self.optional+108): return (0, 0)
        at = self.optional+112+index*8
        return (self.u32(at), self.u32(at+4))

    def imports(self):
        rva, size = self.directory(1)
        result = []
        if not rva or not size: return result
        terminated = False
        for i in range(size//20):
            at = self.offset(rva+i*20, 20)
            if self.slice(at, 20) == bytes(20):
                terminated = True
                break
            dll = self.string(self.u32(at+12))
            lookup = self.u32(at) or self.u32(at+16)
            first = self.u32(at+16)
            functions = []
            for j in range(65536):
                value = self.u64(self.offset(lookup+j*8, 8))
                if not value: break
                functions.append('ordinal:'+str(value & 0xffff) if value >> 63 else self.string(value+2))
                self.iat[first+j*8] = functions[-1]
            else: raise ValueError('Unterminated import thunk')
            result.append({'dll': dll, 'functions': functions})
        assert terminated, 'Unterminated import descriptors'
        return result

def occurrences(data, needle):
    data, needle = data.lower(), needle.lower()
    matches, start = [], 0
    while True:
        at = data.find(needle, start)
        if at < 0: return matches
        matches.append(at)
        start = at+1

def inspect(path, with_capstone=False):
    data = path.read_bytes()
    pe = PE(data)
    imports = pe.imports()
    names = {name for dll in imports for name in dll['functions']}
    result = {
        'file': path.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
        'machine': hex(pe.u16(pe.pe+4)), 'isDLL': bool(pe.u16(pe.pe+22) & 0x2000),
        'subsystem': pe.u16(pe.optional+68), 'sections': pe.sections,
        'importedDLLs': len(imports), 'importedFunctions': sum(len(d['functions']) for d in imports),
        'selectedImportCapabilities': {group: {name: name in names for name in tests} for group, tests in GROUPS.items()},
        'delayImportDirectory': dict(zip(('rva', 'bytes'), pe.directory(13))),
        'CLRDirectory': dict(zip(('rva', 'bytes'), pe.directory(14))),
        'fixedTermOccurrences': {term: {'asciiOffsets': occurrences(data, term.encode('ascii')), 'utf16leOffsets': occurrences(data, term.encode('utf-16le'))} for term in TERMS},
        'limits': 'Import capability and word matches do not establish execution or a working anti-cheat bypass. Dynamically resolved/downloaded functionality is outside this static check.',
    }
    if with_capstone:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
        disassembler = Cs(CS_ARCH_X86, CS_MODE_64)
        disassembler.skipdata = True
        selected = {name for tests in GROUPS.values() for name in tests}
        counts = {name: 0 for name in sorted(selected & names)}
        base = pe.u64(pe.optional+24)
        scanned = 0
        skipdata = 0
        for section in pe.sections:
            if not section['characteristics'] & 0x20000000: continue
            code = pe.slice(section['offset'], section['bytes'])
            for address, size, mnemonic, operands in disassembler.disasm_lite(code, base+section['rva']):
                scanned += size
                if mnemonic == '.byte': skipdata += size
                if mnemonic not in ('call', 'jmp'): continue
                match = re.fullmatch(r'qword ptr \[rip(?: ([+-]) (0x[0-9a-f]+))?\]', operands)
                if not match: continue
                displacement = int(match.group(2), 16) if match.group(2) else 0
                if match.group(1) == '-': displacement = -displacement
                name = pe.iat.get(address+size+displacement-base)
                if name in counts: counts[name] += 1
        result['limitedDirectIATReferences'] = {'selectedCallOrJumpCounts': counts, 'linearBytesCovered': scanned, 'skipdataBytes': skipdata, 'method': 'Linear x64 disassembly of executable file-backed sections; direct RIP-relative call/jump references to selected IAT slots only. Counts are static references, not executed calls. Indirect wrappers, computed pointers, data/code ambiguity, dynamic resolution and runtime state are not resolved. No instructions or bypass implementation exported.'}
    return result

def assess(with_capstone=False):
    files, comparisons = [], []
    manifest = json.loads((ROOT/'evidence/artifact-manifest.json').read_text(encoding='utf-8-sig'))
    expected = {item['path']: item['sha256'] for item in manifest}
    for edition, padding in (('Enhanced', 2334), ('Legacy', 2675)):
        for folder, form in (('', 'packed'), ('artifacts/unpacked', 'unpacked')):
            vp = ROOT/folder/f'VIP-{edition}.{form}.dll'
            mp = ROOT/folder/f'MVP-{edition}.{form}.dll'
            vip, mvp = vp.read_bytes(), mp.read_bytes()
            for path, data in ((vp, vip), (mp, mvp)):
                assert hashlib.sha256(data).hexdigest() == expected[path.relative_to(ROOT).as_posix()]
            tail = mvp[len(vip):]
            assert mvp[:len(vip)] == vip and tail == b' '*padding
            comparisons.append({'edition': edition, 'form': form, 'vipPrefixIdentical': True, 'extraBytes': len(tail), 'extraByteValues': sorted(set(tail)), 'containsExtraExecutableSection': False})
        files.append(inspect(ROOT/'artifacts/unpacked'/f'MVP-{edition}.unpacked.dll', with_capstone))
    return {'method': 'Fresh file hashes, whole-file VIP/MVP prefix comparisons, exact overlay bytes, bounded PE32+ section/import parsing and case-insensitive selected ASCII/UTF-16 literal checks. No execution, hooks, memory reads, network interception or bypass extraction.', 'comparisons': comparisons, 'MVPImages': files, 'conclusion': 'No MVP-exclusive executable content identified in either captured edition. A functioning BattlEye bypass is not demonstrated or disproved by these static checks. Ban causation was not assessed.'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-capstone', action='store_true', help='Add limited static IAT-reference counts; requires the capstone Python package.')
    arguments = parser.parse_args()
    print(json.dumps(assess(arguments.with_capstone), indent=2))
