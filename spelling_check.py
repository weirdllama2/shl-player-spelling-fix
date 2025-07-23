import requests
import csv
import re

# --- Config
SEASON = 83  # Change this once per season
PORTAL_PLAYERS_URL = "https://portal.simulationhockey.com/api/v1/players"
INDEX_API_URL = f"https://index.simulationhockey.com/api/v1/players/ratings?season={SEASON}"
OUTPUT_CSV_FILE = "spelling_mismatches.csv"

# --- Normalize names for better comparison
def normalize_for_comparison(name: str) -> str:
    if not name:
        return ""
    name = name.lower()
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'").replace("´", "'")
    name = re.sub(r"[–—]", "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

# --- Fetch Portal player data
def fetch_portal_players():
    response = requests.get(PORTAL_PLAYERS_URL)
    response.raise_for_status()
    return response.json()

# --- Fetch Index player ratings for a given season
def fetch_index_players():
    response = requests.get(INDEX_API_URL)
    response.raise_for_status()
    return response.json()

# --- Build mapping from index ID to portal name
def build_portal_mapping(portal_players):
    mapping = {}
    for player in portal_players:
        index_records = player.get("indexRecords") or []
        for record in index_records:
            if record.get("leagueID") == 0:  # SHL only
                mapping[record["indexID"]] = player["name"]
    return mapping

# --- Main comparison and CSV export
def main():
    print("🔄 Fetching Portal player data...")
    portal_players = fetch_portal_players()

    print(f"🔄 Fetching Index player ratings for S{SEASON}...")
    index_players = fetch_index_players()

    portal_mapping = build_portal_mapping(portal_players)

    rows = []
    header = ["Index ID", "Portal Name", "Index Name", "Mismatch"]

    for index_player in index_players:
        index_id = index_player["id"]
        index_name = index_player["name"]
        portal_name = portal_mapping.get(index_id)

        if not portal_name:
            continue  # Skip if no Portal match

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
