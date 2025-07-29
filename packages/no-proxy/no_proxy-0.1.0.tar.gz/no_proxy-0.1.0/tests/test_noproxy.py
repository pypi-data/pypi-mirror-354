import no_proxy


def test_bypass():
    assert all(
        map(
            lambda host: no_proxy.bypass("*", host),
            ("example.com", "127.0.0.1", "2001:db8::1"),
        )
    )
    assert all(
        map(
            lambda host: no_proxy.bypass(
                "127.0.0.1/8,10.0.0.1,2001:db8::/32,::1", host
            ),
            ("127.0.0.1", "127.0.0.255", "10.0.0.1", "2001:db8::1", "0000::1"),
        )
    )
    assert all(
        map(
            lambda host: no_proxy.bypass(".example.org,example.com", host),
            ("example.com", "sub.example.org"),
        )
    )


def test_dont_bypass():
    assert all(
        map(
            lambda host: not no_proxy.bypass(
                "127.0.0.1/8,10.0.0.1,2001:db8::/32,::1", host
            ),
            ("128.0.0.1", "::2", "sub.example.org", "localhost"),
        )
    )
    assert all(
        map(
            lambda host: not no_proxy.bypass(".example.org,example.com", host),
            ("www.example.com", "example.org", "127.0.0.1"),
        )
    )
