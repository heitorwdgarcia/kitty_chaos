import json
from collections import Counter, defaultdict

FILE = "telemetry_runs.jsonl"
OUTPUT = "analysis_report.txt"


# =========================================================
# LOAD RUNS
# =========================================================

def load_runs():

    runs = []

    with open(FILE, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                runs.append(json.loads(line))
            except:
                pass

    return runs


# =========================================================
# ANALYZE
# =========================================================

def analyze(runs):

    report = []

    def write(line=""):
        report.append(line)

    total_runs = len(runs)

    if total_runs == 0:
        write("No runs found.")
        return report

    # -------------------------------------------------
    # BASIC STATS
    # -------------------------------------------------

    total_kills = 0
    total_time = 0

    rage_kills = 0
    rage_explosions = 0

    near_misses = 0

    shots = 0
    hits = 0

    death_reasons = Counter()

    upgrades = Counter()
    upgrades_offered = Counter()

    stage_reached = Counter()
    death_stage = Counter()
    death_event = Counter()

    stage_time = defaultdict(list)
    stage_kills = defaultdict(list)
    stage_pressure = defaultdict(list)

    # -------------------------------------------------
    # COLLECT DATA
    # -------------------------------------------------

    for r in runs:

        total_kills += r.get("kills", 0)
        total_time += r.get("run_time", 0)

        rage_kills += r.get("rage_kills", 0)
        rage_explosions += r.get("rage_explosions", 0)

        near_misses += r.get("near_misses", 0)

        shots += r.get("shots_fired", 0)
        hits += r.get("shots_hit", 0)

        death_reasons[r.get("death_reason", "unknown")] += 1

        stage_reached[r.get("stage_reached", 0)] += 1
        death_stage[r.get("death_stage", 0)] += 1

        ev = r.get("death_event")
        if ev:
            death_event[ev] += 1

        times = r.get("stage_time", [])
        kills = r.get("stage_kills", [])
        pressure = r.get("spawn_pressure", [])

        for i in range(len(times)):
            stage_time[i].append(times[i])

        for i in range(len(kills)):
            stage_kills[i].append(kills[i])

        for i in range(len(pressure)):
            stage_pressure[i].append(pressure[i])

        for up in r.get("upgrades_taken", []):
            upgrades[up["name"]] += 1

        for offer in r.get("upgrades_offered", []):
            for u in offer:
                upgrades_offered[u] += 1

    # -------------------------------------------------
    # REPORT
    # -------------------------------------------------

    write("==============================")
    write("RUN STATISTICS")
    write("==============================")

    write(f"Total runs: {total_runs}")
    write(f"Average run time: {total_time/total_runs:.2f}s")
    write(f"Average kills: {total_kills/total_runs:.2f}")

    write()
    write("==============================")
    write("COMBAT")
    write("==============================")

    if shots > 0:
        write(f"Hit rate: {(hits/shots)*100:.1f}%")

    write(f"Total shots: {shots}")
    write(f"Total hits: {hits}")

    write()
    write("==============================")
    write("RAGE SYSTEM")
    write("==============================")

    write(f"Rage explosions: {rage_explosions}")
    write(f"Rage kills: {rage_kills}")

    if rage_explosions > 0:
        write(f"Kills per explosion: {rage_kills/rage_explosions:.2f}")

    write()
    write("==============================")
    write("DODGE SKILL")
    write("==============================")

    write(f"Total near misses: {near_misses}")
    write(f"Near misses per run: {near_misses/total_runs:.2f}")

    write()
    write("==============================")
    write("DEATH REASONS")
    write("==============================")

    for reason, count in death_reasons.most_common():
        write(f"{reason}: {count}")

    write()
    write("==============================")
    write("RUN PROGRESSION")
    write("==============================")

    for stage, count in sorted(stage_reached.items()):

        percent = (count / total_runs) * 100
        write(f"Reached Stage {stage}: {count} runs ({percent:.1f}%)")

    write()
    write("==============================")
    write("DEATH BY STAGE")
    write("==============================")

    for stage, count in sorted(death_stage.items()):

        percent = (count / total_runs) * 100
        write(f"Died at Stage {stage}: {count} runs ({percent:.1f}%)")

    write()
    write("==============================")
    write("DEATH EVENTS")
    write("==============================")

    for ev, count in death_event.most_common():

        percent = (count / total_runs) * 100
        write(f"{ev}: {count} runs ({percent:.1f}%)")

    write()
    write("==============================")
    write("STAGE BALANCE")
    write("==============================")

    max_stage = max(stage_time.keys(), default=-1)

    for i in range(max_stage + 1):

        if not stage_time[i]:
            continue

        avg_frames = sum(stage_time[i]) / len(stage_time[i])
        avg_time = avg_frames / 60

        avg_kills = sum(stage_kills[i]) / len(stage_kills[i])
        avg_pressure = sum(stage_pressure[i]) / len(stage_pressure[i])

        avg_enemies_alive = 0
        if avg_frames > 0:
            avg_enemies_alive = avg_pressure / avg_frames
        
        kills_per_second = 0
        if avg_time > 0:
            kills_per_second = avg_kills / avg_time

        write()
        write(f"Stage {i}")
        write(f"  avg time: {avg_time:.2f}s")
        write(f"  avg kills: {avg_kills:.2f}")
        write(f"  avg enemies alive: {avg_enemies_alive:.2f}")
        write(f"  kills per second: {kills_per_second:.2f}")

    write()
    write("==============================")
    write("UPGRADES CHOSEN")
    write("==============================")

    for up, count in upgrades.most_common():
        write(f"{up}: {count}")

    write()
    write("==============================")
    write("UPGRADE PICK RATE")
    write("==============================")

    for up in upgrades_offered:

        offered = upgrades_offered[up]
        taken = upgrades.get(up, 0)

        rate = 0
        if offered > 0:
            rate = taken / offered * 100

        write(f"{up}: {rate:.1f}% pick rate ({taken}/{offered})")

    return report


# =========================================================
# MAIN
# =========================================================

def main():

    runs = load_runs()

    report = analyze(runs)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for line in report:
            f.write(line + "\n")

    print(f"Analysis saved to {OUTPUT}")


if __name__ == "__main__":
    main()