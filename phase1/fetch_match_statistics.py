import requests
import aiohttp
import asyncio
from db_config import get_connection

API_HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "XXXXXX"
}

async def fetch_statistics(session, match_id):
    url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={match_id}"
    async with session.get(url, headers=API_HEADERS) as response:
        if response.status != 200:
            print(f"Failed to fetch statistics for MatchID {match_id}. Status: {response.status}")
            return None
        return await response.json()

async def process_matches(matches):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_statistics(session, match_id) for match_id, _, _ in matches]
        return await asyncio.gather(*tasks)

def fetch_and_insert_match_statistics():
    conn = get_connection()
    if conn is None:
        return
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT MatchID, HomeTeamID, AwayTeamID 
            FROM Matches 
            WHERE MatchID NOT IN (SELECT MatchID FROM MatchStatistics)
            AND SeasonID IN (SELECT SeasonID FROM Seasons WHERE SeasonYear >= 2020)
            ORDER BY MatchID ASC
        """)
        matches = cur.fetchall()

        if not matches:
            print("No unprocessed matches found.")
            return

        print(f"Processing {len(matches)} matches...")
        
        loop = asyncio.get_event_loop()
        statistics = loop.run_until_complete(process_matches(matches))

        statistics_to_insert = []
        for match_id, home_team_id, away_team_id, stat_data in zip(
            [match[0] for match in matches], 
            [match[1] for match in matches], 
            [match[2] for match in matches], 
            statistics
        ):
            if not stat_data or not stat_data.get("response"):
                print(f"No statistics available for MatchID {match_id}")
                continue

            possession_home = possession_away = 0
            shots_on_target_home = shots_on_target_away = 0
            shots_off_target_home = shots_off_target_away = 0
            corners_home = corners_away = 0
            fouls_home = fouls_away = 0

            for team_stats in stat_data["response"]:
                team_id = team_stats["team"]["id"]
                stats = team_stats["statistics"]

                if team_id == home_team_id:
                    possession_home = int(next((stat["value"].replace('%', '') if stat["value"] else 0 for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots on Goal"), 0)
                    shots_off_target_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots off Goal"), 0)
                    corners_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_home = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Fouls"), 0)

                elif team_id == away_team_id:
                    possession_away = int(next((stat["value"].replace('%', '') if stat["value"] else 0 for stat in stats if stat["type"] == "Ball Possession"), 0))
                    shots_on_target_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots on Goal"), 0)
                    shots_off_target_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Shots off Goal"), 0)
                    corners_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Corner Kicks"), 0)
                    fouls_away = next((stat["value"] if stat["value"] else 0 for stat in stats if stat["type"] == "Fouls"), 0)

            statistics_to_insert.append((
                match_id, possession_home, possession_away, shots_on_target_home, shots_on_target_away,
                shots_off_target_home, shots_off_target_away, corners_home, corners_away, fouls_home, fouls_away
            ))

        cur.executemany("""
            INSERT INTO MatchStatistics (
                MatchID, PossessionHome, PossessionAway, ShotsOnTargetHome, ShotsOnTargetAway,
                ShotsOffTargetHome, ShotsOffTargetAway, CornersHome, CornersAway, FoulsHome, FoulsAway
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (MatchID) DO UPDATE SET
                PossessionHome = EXCLUDED.PossessionHome,
                PossessionAway = EXCLUDED.PossessionAway,
                ShotsOnTargetHome = EXCLUDED.ShotsOnTargetHome,
                ShotsOnTargetAway = EXCLUDED.ShotsOnTargetAway,
                ShotsOffTargetHome = EXCLUDED.ShotsOffTargetHome,
                ShotsOffTargetAway = EXCLUDED.ShotsOffTargetAway,
                CornersHome = EXCLUDED.CornersHome,
                CornersAway = EXCLUDED.CornersAway,
                FoulsHome = EXCLUDED.FoulsHome,
                FoulsAway = EXCLUDED.FoulsAway;
        """, statistics_to_insert)

        conn.commit()
        print("Match statistics inserted successfully!")
    except Exception as e:
        print(f"Error inserting match statistics: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    fetch_and_insert_match_statistics()
