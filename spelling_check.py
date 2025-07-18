import requests
import csv
import re

# API endpoints
PORTAL_PLAYERS_API = "https://portal.simulationhockey.com/api/v1/players"
INDEX_PLAYERS_API = "https://index.simulationhockey.com/api/v1/players"

# Output file
OUTPUT_CSV_FILE = "spelling_mismatches.csv"

def normalize_for_comparison(name: str) -> str:
    """Normalize a name string to make comparison more reliable (ignore punctuation, capitalization, etc.)"""
    if not name:
        return ""
    name = name.lower()
    name = name.replace("’", "'").replace("‘", "'").replace("`", "'").replace("´", "'")
    name = re.sub(r"[–—]", "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def fetch_json_from_api(url):
    """Fetch and parse JSON data from the given API URL."""
    print(f"Fetching: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Error: Got {response.status_code} from {url}")
        response.raise_for_status()
    return response.json()

def build_portal_mapping(portal_players):
    """Create a mapping from Index ID to player name using SHL (leagueID = 0) data."""
    mapping = {}
    for player in portal_players:
        index_records = player.get("indexRecords") or []
        for record in index_records:
            if record.get("leagueID") == 0:  # SHL only
                mapping[record["indexID"]] = player["name"]
    return mapping

def main():
    # Step 1: Fetch players from the portal
    print("📡 Fetching portal players...")
    portal_players = fetch_json_from_api(PORTAL_PLAYERS_API)

    # Step 2: Fetch players from the index
    print("📡 Fetching index players...")
    index_players = fetch_json_from_api(INDEX_PLAYERS_API)

    # Step 3: Build mapping of index ID → portal name
    portal_mapping = build_portal_mapping(portal_players)

    # Step 4: Compare names and collect mismatches
    rows = []
    header = ["Index ID", "Portal Name", "Index Name", "Mismatch"]

    for index_player in index_players:
        index_id = index_player["id"]
        index_name = index_player["name"]
        portal_name = portal_mapping.get(index_id)

        if not portal_name:
            continue  # Skip players not present in portal

        index_norm = normalize_for_comparison(index_name)
        portal_norm = normalize_for_comparison(portal_name)

        if index_norm != portal_norm:
            rows.append([index_id, portal_name, index_name, "Mismatch"])

    # Step 5: Write results to CSV
    with open(OUTPUT_CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"✅ Spelling mismatch report saved to '{OUTPUT_CSV_FILE}' with {len(rows)} entries.")

if __name__ == "__main__":
    main()
