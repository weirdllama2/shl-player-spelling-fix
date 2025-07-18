# SHL Player Name Mismatch Checker

This script compares player names between the Portal system and the SHL Index database to detect spelling mismatches for SHL trading cards. It will create a csv file automatically if the API works. There is a backup version in place that can be run manually if needed.

---

## Files needed (for manual download, only if API doesn't work)

- `players.json` — Exported manually from the Portal system. Grab from here https://portal.simulationhockey.com/api/v1/player
- `index_players.json` — Exported manually from the SHL Index for the relevant season, e.g. for S83 use https://index.simulationhockey.com/api/v1/players/ratings?season=83

Place both files in the same folder as the script.

---

## How to use

1. **Update the JSON files manually:**

   - Export the latest `players.json` from the Portal system.
   - Export the latest `index_players.json` from the SHL Index for the season you want to check.

2. **Run the script locally:**

   ```bash
   python spelling_check_manual.py
