"""comun.clasificar_salidas: missing vs stale vs up-to-date (synthetic files)."""

import comun


def test_missing_stale_and_current_are_told_apart(tmp_path):
    ok = tmp_path / "ok.tex"
    ok.write_text("same", encoding="utf-8")
    stale = tmp_path / "stale.tex"
    stale.write_text("old", encoding="utf-8")
    gone = tmp_path / "gone.tex"

    faltan, desactualizados = comun.clasificar_salidas(
        [(ok, "same"), (stale, "new"), (gone, "x")]
    )
    assert faltan == [gone]
    assert desactualizados == [stale]


def test_all_current(tmp_path):
    f = tmp_path / "a.tex"
    f.write_text("a", encoding="utf-8")
    assert comun.clasificar_salidas([(f, "a")]) == ([], [])
