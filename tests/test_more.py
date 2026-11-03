# =============================================================================
# ELECTRO-HOBBY-3D-UPDATER - tests/test_more.py
# Copyright (C) 2026 JuanenRac (Electro Hobby 3D) <electrohobby3d@gmail.com>
# GPL-3.0-or-later - see LICENSE
# =============================================================================
"""More tests: the words of the window in every language, the reading of versions and tags, and the pins that are odd."""
from __future__ import annotations

import re
import subprocess

import pytest

from electro_hobby_3d_updater import i18n
from electro_hobby_3d_updater.main import _version_tuple
from electro_hobby_3d_updater.pins import Pin, PinReport, describe, latest_tag, read_pins, version_tuple


class _Result:
    def __init__(self, returncode: int = 0, stdout: str = "") -> None:
        self.returncode = returncode
        self.stdout = stdout


def _runner(stdout: str, returncode: int = 0):
    def run(command, **_kwargs):
        assert command[:3] == ["git", "ls-remote", "--tags"]
        return _Result(returncode, stdout)

    return run


# --- the words -----------------------------------------------------------------------------------------------------------


def test_the_eight_languages_are_the_expected_ones_in_order_and_each_has_a_name():
    assert [code for code, _ in i18n.LANGUAGES] == ["en", "es", "de", "fr", "it", "ja", "zh", "pt"]
    assert all(name.strip() for _, name in i18n.LANGUAGES)
    assert len({code for code, _ in i18n.LANGUAGES}) == 8


def test_no_text_is_empty_and_no_marker_is_left_unsubstituted_or_unbalanced():
    for key in i18n.keys():
        for code, _ in i18n.LANGUAGES:
            value = i18n.text(code, key)
            assert value.strip(), (key, code)
            assert value == value.strip(), (key, code, "blanks around the text")
            assert "\n" not in value, (key, code)
            assert value.count("{") == value.count("}"), (key, code)
            assert "TODO" not in value and "XXX" not in value and "%s" not in value, (key, code)


def test_the_placeholders_are_the_same_in_every_language_of_a_key():
    marker = re.compile(r"\{[^{}]*\}")
    for key in i18n.keys():
        reference = sorted(marker.findall(i18n.text("en", key)))
        for code, _ in i18n.LANGUAGES:
            assert sorted(marker.findall(i18n.text(code, key))) == reference, (key, code)


def test_a_text_is_translated_in_the_languages_that_are_not_english_except_the_names_and_labels_that_are_the_same():
    same_allowed = {"title", "about_email_label", "about_license"}
    for key in i18n.keys():
        if key in same_allowed or key.startswith("tag_"):
            continue
        english = i18n.text("en", key)
        others = {code: i18n.text(code, key) for code, _ in i18n.LANGUAGES if code != "en"}
        # a text that is the English one in all seven other languages was not translated
        assert any(v != english for v in others.values()), key


def test_the_ja_and_zh_texts_have_their_own_letters_and_the_others_are_not_in_those_scripts():
    cjk = re.compile(r"[぀-ヿ一-鿿]")
    for key in i18n.keys():
        if key in {"title", "about_license", "about_email_label"} or key.startswith("tag_"):
            continue
        for code in ("ja", "zh"):
            assert cjk.search(i18n.text(code, key)), (key, code)
        for code in ("en", "es", "de", "fr", "it", "pt"):
            assert not cjk.search(i18n.text(code, key)), (key, code)


def test_the_portuguese_is_the_one_of_portugal_where_it_differs_from_the_brazilian_one():
    brazilian = {"arquivo", "atualizar", "tela", "celular", "salvar"}
    for key in i18n.keys():
        words = set(re.findall(r"[a-zà-ú]+", i18n.text("pt", key).lower()))
        assert not (words & brazilian), (key, words & brazilian)


def test_an_unknown_language_is_english_and_an_unknown_key_is_the_key():
    for key in i18n.keys():
        assert i18n.text("xx", key) == i18n.text("en", key)
        assert i18n.text("", key) == i18n.text("en", key)
    assert i18n.text("de", "no-such-key") == "no-such-key"
    assert i18n.text("xx", "") == ""


def test_the_keys_are_unique_and_the_tag_of_each_ecosystem_is_there():
    keys = i18n.keys()
    assert len(keys) == len(set(keys))
    for tag in ("tag_hydra-umc", "tag_urtc", "tag_armor", "tag_eh3d"):
        assert tag in keys


# --- the versions ---------------------------------------------------------------------------------------------------------


def test_a_version_is_read_with_up_to_four_numbers_and_padded_with_zeros():
    assert version_tuple("0.0.3") == (0, 0, 3, 0)
    assert version_tuple("v1.2") == (1, 2, 0, 0)
    assert version_tuple("0.8.0.1") == (0, 8, 0, 1)
    assert version_tuple("1.2.3.4.5") == (1, 2, 3, 4)
    assert version_tuple("nothing") == (0, 0, 0, 0)
    assert version_tuple("") == (0, 0, 0, 0)


def test_versions_are_compared_by_their_numbers_not_by_their_text():
    assert version_tuple("0.0.10") > version_tuple("0.0.9")
    assert version_tuple("0.5.0") > version_tuple("0.4.9")
    assert version_tuple("0.8.1.0") > version_tuple("0.8.0.9")
    assert version_tuple("1.0") == version_tuple("1.0.0.0")


def test_the_version_of_the_window_commands_reads_what_is_in_the_text():
    assert _version_tuple("v1.2.3") == (1, 2, 3)
    assert _version_tuple("updater 0.0.3 (build 7)") == (0, 0, 3, 7)
    assert _version_tuple("none") == ()


# --- the tags -------------------------------------------------------------------------------------------------------------


def test_the_latest_tag_ignores_what_is_not_a_version_and_takes_the_highest_number_with_or_without_v():
    out = "\n".join(
        [
            "aaaaaaa\trefs/tags/v0.0.2",
            "bbbbbbb\trefs/tags/0.0.10",
            "ccccccc\trefs/tags/v0.0.9",
            "ddddddd\trefs/tags/nightly",
            "eeeeeee\trefs/tags/v1.0-rc1",
            "",
        ]
    )
    assert latest_tag("https://github.com/JuanenRac/X", runner=_runner(out)) == "0.0.10"


def test_the_latest_tag_is_none_for_no_tags_a_failed_command_or_a_tool_that_is_missing():
    assert latest_tag("https://x/y", runner=_runner("")) is None
    assert latest_tag("https://x/y", runner=_runner("aaa\trefs/tags/nightly\n")) is None
    assert latest_tag("https://x/y", runner=_runner("aaa\trefs/tags/v1.0.0\n", returncode=128)) is None

    def missing(*_a, **_k):
        raise FileNotFoundError("git")

    def timeout(*_a, **_k):
        raise subprocess.TimeoutExpired("git", 1)

    assert latest_tag("https://x/y", runner=missing) is None
    assert latest_tag("https://x/y", runner=timeout) is None


def test_the_repository_is_asked_with_its_url_and_a_timeout():
    seen = {}

    def run(command, **kwargs):
        seen["command"], seen["kwargs"] = command, kwargs
        return _Result(0, "")

    latest_tag("https://github.com/JuanenRac/X", runner=run, timeout=5.0)
    assert seen["command"][-1] == "https://github.com/JuanenRac/X.git"
    assert seen["kwargs"]["timeout"] == 5.0
    assert seen["kwargs"]["check"] is False


# --- the pins -------------------------------------------------------------------------------------------------------------

_SHA = "0123456789abcdef0123456789abcdef01234567"


def test_a_pin_needs_a_commit_and_a_version_comment_and_the_rest_is_not_a_pin():
    text = "\n".join(
        [
            f'    "eh3d-updater @ git+https://github.com/JuanenRac/EH3D-UPDATER.git@{_SHA}",  # v0.0.3',
            '    "short @ git+https://github.com/JuanenRac/SHORT@abcdef1"  # 1.2',
            f'    "nocomment @ git+https://github.com/JuanenRac/NOC.git@{_SHA}",',
            '    "requests>=2.0",',
            '    "badsha @ git+https://github.com/JuanenRac/BAD.git@xyz1234"  # v1.0',
            "",
        ]
    )
    pins = read_pins(text)
    assert [p.name for p in pins] == ["eh3d-updater", "short"]
    assert pins[0] == Pin("eh3d-updater", "https://github.com/JuanenRac/EH3D-UPDATER", _SHA, "0.0.3")
    assert pins[1].sha == "abcdef1" and pins[1].version == "1.2"
    assert read_pins("") == []


def test_a_pin_with_four_numbers_in_its_version_is_read():
    pins = read_pins(f'"x @ git+https://h/x.git@{_SHA}"  # v0.8.0.1\n')
    assert pins[0].version == "0.8.0.1"


@pytest.mark.parametrize(
    ("pinned", "latest", "behind"),
    [("0.0.3", "0.0.4", True), ("0.0.3", "0.0.3", False), ("0.0.4", "0.0.3", False), ("0.0.9", "0.0.10", True), ("0.8.0", "0.8.0.1", True), ("1.0", "1.0.0.0", False)],
)
def test_a_pin_is_behind_only_when_the_latest_tag_is_higher_by_its_numbers(pinned, latest, behind):
    assert PinReport(Pin("p", "https://h/p", _SHA, pinned), latest).behind is behind


def test_a_pin_whose_repository_cannot_be_reached_is_unknown_and_never_behind():
    report = PinReport(Pin("p", "https://h/p", _SHA, "0.0.1"), None)
    assert report.behind is False
    assert "unknown" in describe(report)
    assert "not reachable" in describe(report)


def test_the_description_of_a_pin_says_which_of_the_three_cases_it_is():
    pin = Pin("p", "https://h/p", _SHA, "0.0.3")
    assert "behind" in describe(PinReport(pin, "0.0.4")) and "v0.0.4" in describe(PinReport(pin, "0.0.4"))
    assert "is the latest tag" in describe(PinReport(pin, "0.0.3"))
    assert describe(PinReport(pin, "0.0.3")).startswith("p: pinned v0.0.3")
