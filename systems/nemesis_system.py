import json
import os

MEMORY_FILE = "nemesis_memory.json"

# memória durante a run
combat_memory = {}

# memória persistente
nemesis_memory = {}


# =========================================================
# LOAD MEMORY
# =========================================================

def load_memory():

    global nemesis_memory

    if not os.path.exists(MEMORY_FILE):

        nemesis_memory = {}

        return

    try:

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:

            nemesis_memory = json.load(f)

    except:

        nemesis_memory = {}


# =========================================================
# SAVE MEMORY
# =========================================================

def save_memory():

    try:

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:

            json.dump(nemesis_memory, f, indent=4)

    except Exception as e:

        print("Nemesis save error:", e)


# =========================================================
# START RUN
# =========================================================

def start_run():

    global combat_memory

    combat_memory = {}

    load_memory()


# =========================================================
# RECORD FIGHT
# =========================================================

def record_fight(profile, stats):

    if profile not in combat_memory:

        combat_memory[profile] = []

    combat_memory[profile].append(stats)


# =========================================================
# MERGE RUN DATA
# =========================================================

def finalize_run():

    global nemesis_memory

    for profile, fights in combat_memory.items():

        if profile not in nemesis_memory:

            nemesis_memory[profile] = {

                "encounters": 0,
                "avg_accuracy": 0,
                "avg_near_miss": 0
            }

        data = nemesis_memory[profile]

        for fight in fights:

            data["encounters"] += 1

            acc = fight.get("accuracy", 0)
            nm = fight.get("near_miss", 0)

            # média simples incremental
            data["avg_accuracy"] = (
                data["avg_accuracy"] + acc
            ) / 2

            data["avg_near_miss"] = (
                data["avg_near_miss"] + nm
            ) / 2

    save_memory()