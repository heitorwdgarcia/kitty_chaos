# Quero uma auditoria completa deste código.

# Siga exatamente este processo:

# 1. Entender o papel do arquivo dentro do sistema
# 2. Mapear dependências (quem chama / quem usa)
# 3. Avaliar impacto na arquitetura geral do jogo
# 4. Identificar problemas antes de sugerir mudanças

# ---

# Analise obrigatoriamente:

# ### 1. Bugs e problemas reais
# - lógica incorreta
# - edge cases
# - comportamento inconsistente
# - possíveis crashes
# - problemas de timing / múltiplas execuções

# ### 2. Arquitetura
# - responsabilidade do arquivo está correta?
# - está violando autoridade de sistemas?
# - lógica deveria estar em outro lugar?
# - está acoplado demais?

# ### 3. Duplicação e redundância
# - código repetido
# - variáveis duplicadas
# - lógica que deveria ser centralizada

# ### 4. Fluxo de dados (MUITO IMPORTANTE)
# - dados estão vindo de onde?
# - estão sendo modificados em múltiplos lugares?
# - existe risco de estado inconsistente?

# ### 5. Autoridade de sistemas
# Verificar se respeita:
# - spawn → spawn.py
# - morte → kill_enemy()
# - run end → run_director
# - telemetria → run_logger

# ### 6. Performance
# - loops desnecessários
# - operações caras
# - crescimento de listas
# - risco em runs longas (bot 1000 runs)

# ### 7. Telemetria
# - dados importantes não sendo registrados?
# - dados inconsistentes?
# - métricas quebradas?

# ### 8. Game Design (alinhado ao GDD)
# - isso quebra pacing da run?
# - afeta near miss?
# - afeta caos controlado?
# - afeta duração (~5 min)?

# ---

# Formato da resposta:

# 1. Problemas encontrados (priorizados)
# 2. Explicação do impacto (técnico + gameplay)
# 3. Plano de correção (antes de codar)

# NÃO implementar ainda.
# Quero primeiro o diagnóstico completo.


import os

ROOT_FOLDER = "."
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