import os

ROOT_FOLDER = r"C:\Users\heito\Documents\Programação\chaos_dodge - v2"
OUTPUT_FILE = "todos_scripts_dump.txt"

IGNORE_FOLDERS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    ".vscode"
}

VALID_EXTENSIONS = {".py"}


def main():

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

        for root, dirs, files in os.walk(ROOT_FOLDER):

            # 🔥 CORREÇÃO PRINCIPAL
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

            files.sort()

            for file in files:

                ext = os.path.splitext(file)[1]

                if ext not in VALID_EXTENSIONS:
                    continue

                path = os.path.join(root, file)

                out.write("\n" + "=" * 80 + "\n")
                out.write(path + "\n")
                out.write("=" * 80 + "\n\n")

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        out.write(f.read())

                except Exception as e:
                    out.write(f"[ERRO AO LER ARQUIVO: {e}]")

                out.write("\n\n")

    print("Dump gerado com sucesso:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()