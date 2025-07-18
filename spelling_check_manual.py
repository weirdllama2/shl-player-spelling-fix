import json
import csv
import re

PORTAL_PLAYERS_FILE = "players.json"
INDEX_PLAYERS_FILE = "index_players.json"
OUTPUT_CSV_FILE = "spelling_mismatches.csv"

def normalize_for_comparison(name: str) -> str:
    if not name:
        return ""
    name = name.lower()
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'").replace("´", "'")
    name = re.sub(r"[–—]", "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def build_portal_mapping(portal_players):
    mapping = {}
    for player in portal_players:
        index_records = player.get("indexRecords") or []
        for record in index_records:
            if record.get("leagueID") == 0:  # SHL only
                mapping[record["indexID"]] = player["name"]
    return mapping

def main():
    print("Loading portal players...")
    portal_players = load_json_file(PORTAL_PLAYERS_FILE)

    print("Loading index players...")
    index_players = load_json_file(INDEX_PLAYERS_FILE)

    portal_mapping = build_portal_mapping(portal_players)

    rows = []
    header = ["Index ID", "Portal Name", "Index Name", "Mismatch"]

    for index_player in index_players:
        index_id = index_player["id"]
        index_name = index_player["name"]
        portal_name = portal_mapping.get(index_id)

        if not portal_name:
            continue  # Ignore missing portal records

        index_norm = normalize_for_comparison(index_name)
        portal_norm = normalize_for_comparison(portal_name)

        if index_norm != portal_norm:
            rows.append([index_id, portal_name, index_name, "Mismatch"])

    with open(OUTPUT_CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"✅ Spelling mismatch report saved to '{OUTPUT_CSV_FILE}' with {len(rows)} entries.")

if __name__ == "__main__":
    main()
