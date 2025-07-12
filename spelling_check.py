import requests
import csv
import argparse

API_PORTAL = "https://portal.simulationhockey.com/api/v1/player"
API_INDEX_RATINGS = "https://index.simulationhockey.com/api/v1/players/ratings"

def fetch_portal_players():
    print("Fetching portal players...")
    res = requests.get(API_PORTAL)
    res.raise_for_status()
    players = res.json()
    # Build indexID to (portal_name, portal_pid) map
    mapping = {}
    for p in players:
        portal_name = p.get("name")
        portal_pid = p.get("pid")
        index_records = p.get("indexRecords", [])
        for rec in index_records:
            if rec.get("leagueID") == 0:  # only SHL league index ids
                index_id = rec.get("indexID")
                mapping[index_id] = (portal_name, portal_pid)
    return mapping

def fetch_index_players(season, league):
    print(f"Fetching index players for season {season}, league {league}...")
    params = {"season": season, "league": league}
    res = requests.get(API_INDEX_RATINGS, params=params)
    res.raise_for_status()
    return res.json()

def compare_and_write_csv(mapping, index_players, season, league):
    filename = f"spelling_issues_season{season}_league{league}.csv"
    print(f"Saving results to {filename}...")
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ["portal_pid", "portal_name", "index_id", "index_name", "spelling_issue"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for p in index_players:
            index_id = p.get("id")
            index_name = p.get("name")
            if index_id in mapping:
                portal_name, portal_pid = mapping[index_id]
                spelling_issue = "NO" if portal_name == index_name else "YES"
                writer.writerow({
                    "portal_pid": portal_pid,
                    "portal_name": portal_name,
                    "index_id": index_id,
                    "index_name": index_name,
                    "spelling_issue": spelling_issue
                })
    print("Done.")

def main():
    parser = argparse.ArgumentParser(description="Check SHL player name spellings between Portal and Index")
    parser.add_argument("--season", type=int, default=83, help="Season to check (default: 83)")
    parser.add_argument("--league", type=int, default=0, help="League to check (default: 0)")
    args = parser.parse_args()

    portal_mapping = fetch_portal_players()
    index_players = fetch_index_players(args.season, args.league)
    compare_and_write_csv(portal_mapping, index_players, args.season, args.league)

if __name__ == "__main__":
    main()
