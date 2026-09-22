"""Lo que comparten tools/gen_days.py (los cuadernos de frases y de
"Leo con lupa") y tools/lupa.py (las actividades propias de "Leo con
lupa"): el error de contenido y el escapado de texto libre a LaTeX. Vive
aparte para que lupa.py no tenga que importar gen_days.py (que a su vez
importa lupa.py)."""


class ErrorDeContenido(Exception):
    """Un día no cumple las reglas -- el mensaje ya dice cuál y por qué."""


def escapar(texto):
    """Escapa los caracteres especiales de LaTeX en texto libre (JSON)."""
    if texto is None:
        return ""
    sustituciones = [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]
    for viejo, nuevo in sustituciones:
        texto = texto.replace(viejo, nuevo)
    return texto


def campos_requeridos(dia_num, actividad, campos):
    faltan = [c for c in campos if c not in actividad]
    if faltan:
        raise ErrorDeContenido(
            f"día {dia_num}: la actividad {actividad.get('tipo')!r} "
            f"necesita {faltan}"
        )
