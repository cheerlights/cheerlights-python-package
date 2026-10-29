"""The package against a fake feed, plus one opt-in check against the live feed (pytest -m live)."""

from __future__ import annotations

from typing import Any

import pytest
import requests

import cheerlights_api
from cheerlights_api import cheerlights_api as module

# Oldest first, the way ThingSpeak returns them; HEX values as the feed publishes them.
FEEDS = [
    {"created_at": "2026-10-27T15:02:00Z", "entry_id": 1, "field1": "red", "field2": "#ff0000"},
    {"created_at": "2026-10-27T16:00:00Z", "entry_id": 2, "field1": "orange", "field2": "#ffa500"},
    {"created_at": "2026-10-27T17:00:00Z", "entry_id": 3, "field1": "green", "field2": "#008000"},
]


class FakeResponse:
    def __init__(self, payload: Any, status: int = 200) -> None:
        self.payload, self.status_code = payload, status

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Server Error")

    def json(self) -> Any:
        return self.payload


@pytest.fixture
def calls(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    """Serve FEEDS from a fake requests.get and record each call."""
    seen: list[dict[str, Any]] = []

    def fake_get(url: str, **kwargs: Any) -> FakeResponse:
        seen.append({"url": url, **kwargs})
        results = kwargs["params"]["results"]
        return FakeResponse({"channel": {"id": 1417}, "feeds": FEEDS[-results:]})

    monkeypatch.setattr(module.requests, "get", fake_get)
    return seen


def serve(monkeypatch: pytest.MonkeyPatch, response: FakeResponse) -> None:
    monkeypatch.setattr(module.requests, "get", lambda url, **kwargs: response)


def test_current_color_is_the_newest_change(calls: list[dict[str, Any]]) -> None:
    assert cheerlights_api.get_current_color() == {"color": "green", "hex": "#008000"}
    assert cheerlights_api.get_current_color_name() == "green"
    assert cheerlights_api.get_current_hex() == "#008000"
    assert calls[0]["url"] == "https://api.thingspeak.com/channels/1417/feed.json"
    assert calls[0]["params"] == {"results": 1}


def test_every_request_has_a_timeout(calls: list[dict[str, Any]]) -> None:
    cheerlights_api.get_current_color()
    cheerlights_api.get_color_history(2)
    assert all(call["timeout"] == module.TIMEOUT for call in calls)


def test_history_is_oldest_first_with_times(calls: list[dict[str, Any]]) -> None:
    history = cheerlights_api.get_color_history(3)
    assert [h["color"] for h in history] == ["red", "orange", "green"]
    assert history[0] == {"color": "red", "hex": "#ff0000", "timestamp": "2026-10-27T15:02:00Z"}
    assert calls[0]["params"] == {"results": 3}


@pytest.mark.parametrize("count", [0, -1, 8001, 2.5, "5", True])
def test_history_count_must_be_1_to_8000(calls: list[dict[str, Any]], count: Any) -> None:
    with pytest.raises(ValueError, match="1 to 8000"):
        cheerlights_api.get_color_history(count)
    assert calls == []


def test_the_name_and_the_feed_agree_on_every_color() -> None:
    # The palette's HEX values are the ones the feed publishes, so a lookup matches the live value.
    assert len(cheerlights_api.COLORS) == 11
    for name, value in cheerlights_api.COLORS.items():
        assert cheerlights_api.color_name_to_hex(name) == value
        assert value == value.lower() and len(value) == 7


def test_green_is_the_cheerlights_green() -> None:
    assert cheerlights_api.color_name_to_hex("green") == "#008000"


def test_names_ignore_case_and_spaces_and_know_the_old_name() -> None:
    assert cheerlights_api.color_name_to_hex("Old Lace") == "#fdf5e6"
    assert cheerlights_api.color_name_to_hex("WarmWhite") == "#fdf5e6"
    assert cheerlights_api.is_valid_color(" Purple ")
    assert cheerlights_api.color_name_to_hex("black") is None
    assert not cheerlights_api.is_valid_color("lime")


def test_hex_to_rgb() -> None:
    assert cheerlights_api.hex_to_rgb("#ffa500") == (255, 165, 0)
    assert cheerlights_api.hex_to_rgb("FDF5E6") == (253, 245, 230)
    for bad in ["#fff", "#gggggg", "", "#ff00001"]:
        with pytest.raises(ValueError):
            cheerlights_api.hex_to_rgb(bad)


def test_a_missing_hex_falls_back_to_the_palette(monkeypatch: pytest.MonkeyPatch) -> None:
    old_entry = {"created_at": "2016-01-01T00:00:00Z", "field1": "warmwhite"}
    serve(monkeypatch, FakeResponse({"feeds": [old_entry]}))
    assert cheerlights_api.get_current_color() == {"color": "warmwhite", "hex": "#fdf5e6"}


def test_an_empty_feed_is_a_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    serve(monkeypatch, FakeResponse({"feeds": []}))
    with pytest.raises(LookupError, match="no color"):
        cheerlights_api.get_current_color()


def test_a_feed_outage_raises_the_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    serve(monkeypatch, FakeResponse("unavailable", status=503))
    with pytest.raises(requests.HTTPError, match="503"):
        cheerlights_api.get_current_color()


def test_the_old_import_path_still_works() -> None:
    from cheerlights_api.cheerlights_api import get_current_color

    assert get_current_color is cheerlights_api.get_current_color


@pytest.mark.live
def test_live_feed() -> None:
    current = cheerlights_api.get_current_color()
    assert cheerlights_api.is_valid_color(current["color"])
    assert cheerlights_api.color_name_to_hex(current["color"]) == current["hex"]
    history = cheerlights_api.get_color_history(5)
    assert len(history) == 5
    assert history == sorted(history, key=lambda h: h["timestamp"])
