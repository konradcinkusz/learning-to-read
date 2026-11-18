"""Negative and positive tests for tools/checklog.py (synthetic logs)."""

import pytest

from conftest import run_tool

CLEAN = "This is LuaTeX, Version 1.18\nOutput written on main.pdf (270 pages).\n"


def write_log(tmp_path, body):
    p = tmp_path / "t.log"
    p.write_text(body, encoding="utf-8")
    return p


def test_clean_log_passes(tmp_path):
    r = run_tool("checklog.py", write_log(tmp_path, CLEAN))
    assert r.returncode == 0
    assert "OK" in r.stdout


def test_file_line_error_is_detected(tmp_path):
    log = write_log(tmp_path, CLEAN + "./main.tex:42: Undefined control sequence.\n")
    r = run_tool("checklog.py", log)
    assert r.returncode == 1
    assert "main.tex:42" in r.stderr


def test_bang_prefix_alone_is_not_how_errors_look(tmp_path):
    # With -file-line-error the line starts with a path, not "!"; this is
    # the regression the script exists for.
    log = write_log(tmp_path, "content/generated-days.tex:7: Missing $ inserted.\n")
    assert run_tool("checklog.py", log).returncode == 1


def test_fatal_error_is_detected(tmp_path):
    log = write_log(tmp_path, CLEAN + "Fatal error occurred, no output PDF file produced!\n")
    r = run_tool("checklog.py", log)
    assert r.returncode == 1
    assert "Fatal error" in r.stderr


@pytest.mark.parametrize("kind", ["hbox", "vbox"])
def test_overfull_boxes_fail(tmp_path, kind):
    log = write_log(tmp_path, CLEAN + f"Overfull \\{kind} (12.3pt too wide) in paragraph at lines 5--6\n")
    r = run_tool("checklog.py", log)
    assert r.returncode == 1
    assert "OVERFULL" in r.stderr


def test_missing_glyph_fails(tmp_path):
    log = write_log(tmp_path, CLEAN + "Missing character: There is no \u2605 in font Andika-Regular!\n")
    r = run_tool("checklog.py", log)
    assert r.returncode == 1
    assert "Missing character" in r.stderr


def test_underfull_is_not_blocking(tmp_path):
    log = write_log(tmp_path, CLEAN + "Underfull \\hbox (badness 10000) in paragraph at lines 1--2\n")
    r = run_tool("checklog.py", log)
    assert r.returncode == 0
    assert "underfull" in r.stdout


def test_missing_file_fails(tmp_path):
    r = run_tool("checklog.py", tmp_path / "nope.log")
    assert r.returncode == 1
    assert "no existe" in r.stderr


def test_no_arguments_is_usage_error():
    assert run_tool("checklog.py").returncode == 2


def test_one_bad_log_among_good_ones_fails(tmp_path):
    good = write_log(tmp_path, CLEAN)
    bad = tmp_path / "bad.log"
    bad.write_text("a.tex:1: Oops.\n", encoding="utf-8")
    assert run_tool("checklog.py", good, bad).returncode == 1
