import ipaddress
from typing import Literal, Sequence, Union


class Dotted(str):
    """Represents a domain and matches any hostname that is a subdomain."""

    def __repr__(self):
        return f"Dotted({super().__repr__()})"

    def matches(self, host: str) -> bool:
        return host.lower().endswith(f".{self.lower()}")


NoProxy = Union[Literal["*"], Sequence["NoProxySingle"]]
"""Represents a complete no-proxy configuration."""

NoProxySingle = Union[
    ipaddress.IPv6Network,
    ipaddress.IPv4Network,
    Dotted,
    str,
]
"""Represents a no-proxy entry. Note that IPv6 (IPv4) addresses are treated as /128 (/32) networks."""


def parse(no_proxy: str) -> NoProxy:
    """Parse a no-proxy string. Examples:
    >>> parse("*")
    '*'
    >>> parse("10.0.0.1,2001:0db8:0000::/32")
    (IPv4Network('10.0.0.1/32'), IPv6Network('2001:db8::/32'))
    >>> parse("example.com,.example.org")
    ('example.com', Dotted('example.org'))
    """

    if no_proxy == "*":
        return "*"

    return (*map(parse_single, no_proxy.split(",")),)


def parse_single(no_proxy_single: str) -> NoProxySingle:
    """Parse a no-proxy entry. Examples:
    >>> parse_single("10.0.0.1")
    IPv4Network('10.0.0.1/32')
    >>> parse_single(".example.org")
    Dotted('example.org')
    """
    try:
        return ipaddress.IPv6Network(no_proxy_single, strict=False)
    except ValueError:
        pass

    try:
        return ipaddress.IPv4Network(no_proxy_single, strict=False)
    except ValueError:
        pass

    return (
        Dotted(no_proxy_single[1:])
        if no_proxy_single.startswith(".")
        else no_proxy_single
    )


def match(no_proxy: NoProxy, host: str) -> bool:
    """Check if a host matches a no-proxy configuration."""
    if no_proxy == "*":
        return True

    return any(match_single(no_proxy_single, host) for no_proxy_single in no_proxy)


def match_single(no_proxy_single: NoProxySingle, host: str) -> bool:
    """Check if a host matches a no-proxy entry."""
    if isinstance(no_proxy_single, (ipaddress.IPv6Network, ipaddress.IPv4Network)):
        try:
            return ipaddress.ip_address(host) in no_proxy_single
        except ValueError:
            return False

    return (
        no_proxy_single.matches(host)
        if isinstance(no_proxy_single, Dotted)
        else host.lower() == no_proxy_single.lower()
    )


def bypass(no_proxy: str, host: str) -> bool:
    """Check if a host should bypass proxies based on a no-proxy string."""
    return match(parse(no_proxy), host)
