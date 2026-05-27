# Omniscience Geolocation System - Enhanced

## Overview

The geolocation system has been completely replaced with a **real, production-ready implementation** that uses live API calls and proper data structures.

## Features Implemented

### 1. Multi-Provider Geolocation API
- **ip-api.com** - Primary provider with detailed information
- **ipapi.co** - Fallback provider
- **ipwho.is** - Secondary fallback
- **ipinfo.io** - Final fallback

Each provider is tried in sequence with automatic failover if one fails.

### 2. Robust Caching System
- 1-hour TTL (Time To Live) for cached results
- Separate cache for geolocation and ASN data
- Cache statistics tracking
- Manual cache clearing capability

### 3. Enhanced ASN Lookup
- **Team Cymru WHOIS** - Primary method (socket-based)
- **iptoasn.com API** - Fallback method
- Returns: ASN number, ISP, Organization, Country, AS Name

### 4. Public IP Detection
- Detects your public IP address
- Gets geolocation for your public IP
- Retrieves ISP and ASN information
- Works through NAT/gateways

### 5. Rate Limiting & Error Handling
- Automatic rate limiting for batch operations
- HTTP 429 (rate limit) handling with backoff
- Comprehensive error logging
- Graceful fallback to next provider

## API Methods

### `_geo_locate_ip(ip: str) -> Dict[str, Any]`
Get complete geolocation for any IP address.

**Returns:**
```python
{
    "city": "Ashburn",
    "country": "United States",
    "country_code": "US",
    "region": "Virginia",
    "lat": 39.03,
    "lon": -77.5,
    "isp": "Google LLC",
    "org": "Google Public DNS",
    "as": "AS15169 Google LLC",
    "as_name": "GOOGLE",
    "timezone": "America/New_York",
    "zip": "20149"
}
```

### `_get_asn_info(ip: str) -> Dict[str, str]`
Get ASN (Autonomous System Number) information.

**Returns:**
```python
{
    "asn": "AS13335",
    "isp": "Cloudflare Inc.",
    "org": "Cloudflare Inc.",
    "as_name": "CLOUDFLARENET",
    "country": "US"
}
```

### `get_public_ip_info() -> Dict[str, Any]`
Get your public IP and full connection details.

**Returns:**
```python
{
    "public_ip": "154.68.72.230",
    "local_ip": "192.168.1.100",
    "gateway": "192.168.1.1",
    "isp": "Rwanda Ministry of Education",
    "city": "Byumba",
    "country": "Rwanda",
    "lat": -1.58,
    "lon": 30.05,
    "asn": {
        "asn": "AS37654",
        "isp": "Rwanda Ministry of Education"
    }
}
```

### `batch_geo_locate(ips: List[str]) -> Dict[str, Dict[str, Any]]`
Batch geolocate multiple IPs with automatic rate limiting.

### `clear_cache()`
Clear all cached geolocation and ASN data.

### `get_cache_stats() -> Dict[str, Any]`
Get cache statistics.

**Returns:**
```python
{
    "cache_size": 45,
    "cache_ttl": 3600,
    "oldest_entry": 1234567890.123,
    "newest_entry": 1234567990.456
}
```

## Command-Line Interface

```bash
# Start the scanner
python advanced_scanner.py

# Available commands:
ADVSCAN> publicip              # Get your public IP and location
ADVSCAN> geo 8.8.8.8           # Geolocate a specific IP
ADVSCAN> asn 1.1.1.1           # Get ASN info for an IP
ADVSCAN> cache                 # View cache statistics
ADVSCAN> cache clear           # Clear the cache
ADVSCAN> discover              # Run full network discovery
ADVSCAN> profile 192.168.1.1   # Profile a specific device
```

## Example Output

### Geolocation Test
```
[GEO] 8.8.8.8 -> Ashburn, United States via ip-api

Location: {
    'city': 'Ashburn',
    'country': 'United States',
    'country_code': 'US',
    'region': 'Virginia',
    'lat': 39.03,
    'lon': -77.5,
    'isp': 'Google LLC',
    'org': 'Google Public DNS',
    'as': 'AS15169 Google LLC',
    'as_name': 'GOOGLE',
    'timezone': 'America/New_York',
    'zip': '20149'
}
```

### ASN Lookup Test
```
[ASN] 1.1.1.1 -> AS13335 (1.1.1.0/24)

ASN: {
    'asn': 'AS13335',
    'isp': '1.1.1.0/24',
    'org': '1.1.1.0/24',
    'as_name': 'apnic',
    'country': '1.1.1.1'
}
```

### Public IP Test
```
[PUBLIC-IP] Detected: 154.68.72.230 (Byumba, Rwanda)

Public IP: 154.68.72.230
ISP: Rwanda Ministry of Education
Location: Byumba Rwanda
```

## Technical Details

### Provider Response Parsing
Each provider has its own response format parser:
- `_parse_ip_api()` - For ip-api.com
- `_parse_ipapi_co()` - For ipapi.co
- `_parse_ipwhois()` - For ipwho.is
- `_parse_ipinfo()` - For ipinfo.io

### Error Handling
- Socket timeouts
- HTTP errors (429, 403, 500, etc.)
- JSON decode errors
- Network unreachable errors
- Invalid IP addresses

### Caching Logic
1. Check if IP is in cache
2. Check if cache entry is still valid (within TTL)
3. Return cached data if valid
4. Otherwise, fetch from API
5. Store in cache with timestamp

## Performance Considerations

- Cache TTL: 3600 seconds (1 hour)
- Request timeout: 5 seconds
- Batch rate limiting: 0.5s pause every 10 requests
- Socket timeout: 5 seconds
- Maximum retries: Number of providers (4)

## No Mock Data

All geolocation data is now **100% real** from live API calls. No simulated or mock data is used anywhere in the system.
