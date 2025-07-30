"""The main test."""

from __future__ import annotations

import ssl

import truststore
import urllib3


def test_truststore_autorun() -> None:
    """Test that truststore is injected."""
    assert ssl.SSLContext is truststore.SSLContext
    assert urllib3.util.ssl_.SSLContext is truststore.SSLContext
