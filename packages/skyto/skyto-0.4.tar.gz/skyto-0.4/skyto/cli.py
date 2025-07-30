import sys
from skyto.interpreter import executer

def main():
    if len(sys.argv) < 2:
        print("Usage: skyto <fichier.sto>")
        return

    fichier_path = sys.argv[1]
    print(f"Traitement du fichier: {fichier_path}")  # Debug
    
    try:
        with open(fichier_path, 'r') as fichier:
            code = fichier.read()
            executer(code)
    except FileNotFoundError:
        print(f"Fichier introuvable : {fichier_path}")
    except Exception as e:
        print(f"ERREUR FATALE: {str(e)}")

if __name__ == "__main__":
    main()