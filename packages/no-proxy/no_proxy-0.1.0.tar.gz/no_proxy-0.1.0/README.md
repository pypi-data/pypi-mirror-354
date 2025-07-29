[![](https://github.com/bachorp/no-proxy/actions/workflows/test.yaml/badge.svg)](https://github.com/bachorp/no-proxy/actions/workflows/test.yaml)
[![](https://img.shields.io/pypi/pyversions/no-proxy)](https://www.python.org)
[![](https://img.shields.io/pypi/v/no-proxy.svg)](https://pypi.org/project/no-proxy/)

# `no-proxy`

Standalone `no_proxy`/`NO_PROXY` parser and evaluator.

## Usage

```python
from no_proxy import bypass # More specific functions and types available
from urllib.parse import urlparse

bypass(no_proxy="*", host="example.com") # True
bypass("127.0.0.0/8,::1", "127.0.0.1") # True

my_host = urlparse("//example.com:5000/path?x=y").hostname # example.com
bypass("www.example.com,example.org", my_host) # False
```

## Specification

A *no-proxy string* is either `*` or a comma-separated list of *no-proxy entries*.
An IP-address or hostname matches a no-proxy string if the string is `*` or if any of its entries matches.

A no-proxy entry is either
- an IP-address, which matches itself,
- an IP-range, which matches included IP-addresses,
- a domain with leading `.`, which matches all of its subdomains, or
- a hostname, which matches itself.

Hostnames are not validated and there is no special handling of whitespace, trailing dots, ports, etc.
