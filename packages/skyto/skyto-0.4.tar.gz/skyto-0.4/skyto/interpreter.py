import re

def traduire_linga_vers_python(code_skyto):
    traduction = {
        "monisa": "print",
        "soki": "if",
        "sokite": "else",
        "pamba_na": "for",
        "kati_na": "in",
        "tala": "def",
        "zongisa": "return",
        "solo": "True",
        "lokuta": "False",
        "benga": "import"
    }

    lignes = code_skyto.split("\n")
    code_python = []

    for ligne in lignes:
        indentation = len(ligne) - len(ligne.lstrip())
        ligne = ligne.strip()
        if not ligne:
            code_python.append("")
            continue

        # Traduction avec limites de mots
        for lingala, python in traduction.items():
            ligne = re.sub(r"\b" + re.escape(lingala) + r"\b", python, ligne)

        # Gestion spéciale de 'print'
        if ligne.startswith("print ") and "(" not in ligne:
            ligne = "print(" + ligne[6:] + ")"

        # Ajout des ':' pour les structures de contrôle
        if ligne.startswith(("if ", "if(", "else", "for ", "for(", "def ", "def(")) and not ligne.endswith(":"):
            ligne += ":"

        code_python.append(" " * indentation + ligne)

    return "\n".join(code_python)


def executer(code_skyto):
    code_python = traduire_linga_vers_python(code_skyto)
    try:
        exec(code_python, globals())
    except Exception as e:
        print(f"Erreur pendant l'exécution du code Skyto :\n{e}")


