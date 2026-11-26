from concurrent.futures import ThreadPoolExecutor

import pytest

from src.warranty_app.config import get_config
from src.warranty_app.portal_rate_limiter import PortalRateLimiter


def test_sliding_window_boundary_and_client_isolation():
    now = [0.0]
    limiter = PortalRateLimiter(2, 60, clock=lambda: now[0])
    assert limiter.consume("client-a") is None
    now[0] = 1
    assert limiter.consume("client-a") is None
    now[0] = 2
    assert limiter.consume("client-a") == 58
    assert limiter.consume("client-b") is None
    now[0] = 60
    assert limiter.consume("client-a") is None
    assert limiter.consume("client-a") == 1


def test_concurrent_attempts_cannot_exceed_limit():
    limiter = PortalRateLimiter(5, 60, clock=lambda: 0.0)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(lambda _: limiter.consume("same-client"), range(30)))
    assert results.count(None) == 5
    assert results.count(60) == 25


def test_client_tracking_is_bounded_and_reclaimed_after_expiry():
    now = [0.0]
    limiter = PortalRateLimiter(1, 60, clock=lambda: now[0], max_clients=2)
    assert limiter.consume("client-a") is None
    assert limiter.consume("client-b") is None
    assert limiter.consume("client-c") == 60
    now[0] = 60
    assert limiter.consume("client-c") is None


def test_rate_limit_configuration_is_read_from_environment(monkeypatch):
    monkeypatch.setenv("PORTAL_LOOKUP_MAX_ATTEMPTS", "12")
    monkeypatch.setenv("PORTAL_LOOKUP_WINDOW_SECONDS", "120")
    config = get_config()
    assert config.portal_lookup_max_attempts == 12
    assert config.portal_lookup_window_seconds == 120


@pytest.mark.parametrize("attempts,window", [(0, 60), (5, 0), (-1, 60)])
def test_invalid_rate_limit_settings_are_rejected(attempts, window):
    with pytest.raises(ValueError):
        PortalRateLimiter(attempts, window)
