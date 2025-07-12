import requests
import csv

def fetch_portal_players():
    url = "https://portal.simulationhockey.com/api/v1/player"
    headers = {
        "User-Agent": "SHL-Player-Spelling-Fix-Bot/1.0"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def fetch_index_players(season=83):
    url = f"https://index.simulationhockey.com/api/v1/players/ratings?league=0&season={season}"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def main():
    print("Fetching portal players...")
    portal_players = fetch_portal_players()
    portal_mapping = {p["pid"]: p["name"] for p in portal_players}

    print("Fetching index players for season 83...")
    index_players = fetch_index_players(83)

    with open("spelling_discrepancies.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["index_id", "index_name", "portal_name", "mismatch"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for player in index_players:
            portal_name = None
            # Find portal player by matching index IDs inside the indexRecords of portal player (if you want)
            # but here we just try to match by pid assuming index id is same as pid or you can adapt.
            pid = player.get("id")
            # In your original example, portal players have "indexRecords" with indexID(s) which we could cross-check
            # For simplicity, if portal player pid == index player id, get name from portal, else leave blank
            portal_name = portal_mapping.get(pid, "")
            mismatch = ""
            if portal_name and portal_name != player["name"]:
                mismatch = "Yes"

            writer.writerow({
                "index_id": player["id"],
                "index_name": player["name"],
                "portal_name": portal_name,
                "mismatch": mismatch
            })

    print("Done. Output saved to spelling_discrepancies.csv")

if __name__ == "__main__":
    main()
