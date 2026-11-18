"""Negative and positive tests for tools/check_pages.py (synthetic .aux)."""

from conftest import run_tool


def aux(days, clave=None):
    """days: {day: page}. Builds the \\newlabel lines LaTeX would write."""
    lines = [f"\\newlabel{{dia:{d}}}{{{{1}}{{{p}}}{{x}}{{y}}{{z}}}}" for d, p in days.items()]
    if clave is not None:
        lines.append(f"\\newlabel{{clave}}{{{{1}}{{{clave}}}{{x}}{{y}}{{z}}}}")
    return "\n".join(lines) + "\n"


def write_aux(tmp_path, days, clave=None):
    p = tmp_path / "t.aux"
    p.write_text(aux(days, clave), encoding="utf-8")
    return p


def test_one_page_per_day_passes(tmp_path):
    r = run_tool("check_pages.py", write_aux(tmp_path, {1: 5, 2: 6, 3: 7}, clave=8))
    assert r.returncode == 0
    assert "OK" in r.stdout


def test_overflowing_day_is_reported_by_number(tmp_path):
    r = run_tool("check_pages.py", write_aux(tmp_path, {1: 5, 2: 6, 3: 8, 4: 9}))
    assert r.returncode == 1
    assert "día 2" in r.stderr
    assert "salto de 2" in r.stderr


def test_missing_day_is_reported(tmp_path):
    r = run_tool("check_pages.py", write_aux(tmp_path, {1: 5, 3: 7}))
    assert r.returncode == 1
    assert "falta el día 2" in r.stderr


def test_last_day_overflowing_into_the_key_is_reported(tmp_path):
    r = run_tool("check_pages.py", write_aux(tmp_path, {1: 5, 2: 6}, clave=8))
    assert r.returncode == 1
    assert "clave de respuestas" in r.stderr


def test_quarter_end_medal_page_is_expected(tmp_path):
    # Day 65 closes a quarter: a medal page follows, so the jump is 2.
    days = {64: 100, 65: 101, 66: 103}
    assert run_tool("check_pages.py", write_aux(tmp_path, days)).returncode == 0


def test_quarter_end_without_medal_page_fails(tmp_path):
    days = {64: 100, 65: 101, 66: 102}
    r = run_tool("check_pages.py", write_aux(tmp_path, days))
    assert r.returncode == 1
    assert "día 65" in r.stderr


def test_aux_without_day_labels_fails(tmp_path):
    p = tmp_path / "empty.aux"
    p.write_text("\\relax\n", encoding="utf-8")
    r = run_tool("check_pages.py", p)
    assert r.returncode == 1
    assert "ninguna etiqueta" in r.stderr


def test_missing_aux_file_fails(tmp_path):
    r = run_tool("check_pages.py", tmp_path / "nope.aux")
    assert r.returncode == 1
    assert "no existe" in r.stderr
