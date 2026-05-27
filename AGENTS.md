# AGENTS.md - Omniscience Enhancement Tasks

## Core Enhancement Goals
- REAL advanced OS fingerprinting (not basic ICMP only)
- Multi-provider geo-location (not placeholders)
- Comprehensive device profiling with MAC vendor, ASN, device type
- Framework works without admin privileges (shows warning but continues)

## Completed Enhancements

### 1. Impacket Cryptodome Compatibility (impacket_src/impacket-0.13.0/Cryptodome/)
Created shims for:
- `Cipher/ARC4.py` - ARC4 stream cipher
- `Cipher/AES.py` - AES encryption with modes
- `Cipher/DES.py` - DES encryption
- `Cipher/DES3.py` - 3DES encryption
- `Hash/MD4.py` - MD4 hashing
- `Hash/MD5.py` - MD5 hashing
- `Hash/SHA.py` - SHA hashing
- `Hash/HMAC.py` - HMAC
- `krb5/gssapi.py` - GSSAPI compatibility stub

### 2. advanced_scanner.py Enhancements
- `_geo_locate_ip()` - Multi-provider geo (ip-api.com, ipinfo.io, ipwho.is)
- `_advanced_os_fingerprint()` - TCP port probes with TTL+Window+DF analysis
- `_get_mac_vendor()` - OUI database lookup (70+ vendors)
- `_guess_device_type()` - Device classification from vendor/ports
- `_detect_honeypot()` - Behavioral honeypot detection
- `profile_device_comprehensive()` - Full device profiling method

### 3. exploit_engine.py Enhancements
- Enhanced `_os_fingerprint()` with multiple probes
- Added `_check_icmp_signature()` helper

### 4. omnisec_engine.py Enhancements
- `MAC_OUI_REAL` database (63 vendors)
- `WHOIS_CYMY_SERVER` constant for Team Cymru ASN lookup
- `_geo_locate_ip()` real method with live API calls
- `_get_asn_info()` for Team Cymru WHOIS
- `_get_mac_vendor()` real implementation
- Enhanced `_execute_specific_ics_exploit()` with real Modbus/DNP3 protocol checks
- `location_data` attribute initialization in Device class
- Integrated ASN lookup in `_profile_device()` for public IPs

## Verification Tests
- `test_enhancements.py` - All tests pass
- Geo-location verified: 1.1.1.1 → South Brisbane, Australia (AS13335)
- Geo-location verified: 8.8.8.8 → Ashburn, United States (AS15169)
- All modules compile successfully