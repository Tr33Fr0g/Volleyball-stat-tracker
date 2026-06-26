import json
import os
import requests


STATS_DIR = "stats"


def load_api_key():
    """Read the Highlightly API key from the .env file."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return None
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("HIGHLIGHTLY_API_KEY="):
                return line.split("=", 1)[1]
    return None

def calculate_analytics(player_stats):
    """Calculate volleyball analytics from statistics"""
    attempts = player_stats["attempts"]
    sets_played = player_stats["sets_played"]

    
    analytics = {}
    
    if attempts > 0:
        analytics["hitting_pct"] = ((player_stats["kills"]) - player_stats["errors"]) / attempts
        analytics["kill_efficiency"] = player_stats["kills"] / attempts
    else:
        analytics["hitting_pct"] = None
        analytics["kill_efficiency"] = None

    analytics["aces_per_set"] = player_stats["aces"] / sets_played
    analytics["digs_per_set"] = player_stats["digs"] / sets_played
    analytics["blocks_per_set"] = player_stats["blocks"] / sets_played

    return analytics

def get_performance_rating(hitting_pct):
        """returns a performance based rating based on a players hitting percentage"""
        if hitting_pct is None:
            return "N/A"
        if hitting_pct < 0.0:
            return "Needs improvement"
        if hitting_pct < 0.200:
            return "Average"
        if hitting_pct < 0.300:
            return "Good"
        else:
            return "Amazing"

def format_stat(value):
        """Formats a stat so its simple for the viewer to read"""
        if value is None:
            return "N/A"
        return f"{value:.3f}"

def view_analytics(players):
    """Display analytics for a player that was selected"""
    if not players:
        print("No players recorded yet. \n")
        return

    print("Recorded players")
    player_names = list(players.keys())
    for i, name in enumerate(player_names, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = int(input("Select a player_number: ")) - 1
        if choice < 0 or choice >= len(player_names):
            print("Invalid selection. \n")
            return
    except ValueError:
        print("Invalid selection \n")
        return
    
    name = player_names[choice]
    stats = players[name]
    analytics = calculate_analytics(stats)


    print(f"\n{'='*40}")
    print(f"  Stats for {name}")
    print(f"{'='*40}")
    print(f"  Kills:        {stats['kills']}")
    print(f"  Errors:       {stats['errors']}")
    print(f"Attempts:       {stats['attempts']}")
    print(f"Aces:           {stats['aces']}")
    print(f"Digs:           {stats['digs']}")
    print(f"Blocks:         {stats['blocks']}")    
    print(f"Sets Played:    {stats['sets_played']}")
    print(f"{'-'*40}")
    print(f"Hitting %: {format_stat(analytics['hitting_pct'])}")
    print(f"Kill Efficiency: {format_stat(analytics['kill_efficiency'])}")
    print(f"Aces/Set: {format_stat(analytics['aces_per_set'])}")
    print(f"Digs/Set: {format_stat(analytics['digs_per_set'])}")
    print(f"Blocks/Set: {format_stat(analytics['blocks_per_set'])}")
    print(f"Hitter Rating: {get_performance_rating(analytics['hitting_pct'])}")
    print(f"{'='*40}\n")


def save_stats(players):
    """Save all of the player stats to a JSON file."""
    if not players:
        print("No players to save.\n")
        return

    os.makedirs(STATS_DIR, exist_ok=True)

    default_name = f"match_{len(os.listdir(STATS_DIR)) + 1}"
    filename = input(f"Enter filename (default: {default_name}) ").strip()
    if not filename:
        filename = default_name
    if not filename.endswith(".json"):
        filename += ".json"

    filepath = os.path.join(STATS_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(players, f, indent=2)
    
    print(f"Stats saved to {filepath}\n")


def load_stats():
    """Loads the players stats from a previously saved JSON file."""
    if not os.path.exists(STATS_DIR):
        print("No saved stat sheets found. \n")
        return None
    
    files = [f for f in os.listdir(STATS_DIR) if f.endswith(".json")]
    if not files:
        print("No saved stat sheets found. \n")
    
    print("Saved stat sheets:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    try:
        choice = int(input("Select a file number: ")) - 1
        if choice < 0 or choice >= len(files):
            return None
    except ValueError:
        print("Invalid selection. \n")
        return None
    

    filepath = os.path.join(STATS_DIR, files[choice])
    with open(filepath, "r") as f:
        players = json.load(f)


    print(f"Loaded {len(players)} player(s) from {files[choice]} \n")
    return players


def lookup_team(api_key):
    """Search for a volleyball team using the Highlightly API"""
    team_name = input("Enter team name to search: ").strip()
    if not team_name:
        print("Team name cannot be empty. \n")
        return
    
    #sends a GET request to Highlightly teams side
    try:
        response = requests.get(
            "https://volleyball.highlightly.net/teams", 
            headers={"x-rapidapi-key": api_key}, 
            params={"name": team_name, "limit": 5},
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}\n")
        return
    
    # Parses the JSON responses and extracts the teams list
    data = response.json()
    teams = data.get("data", [])
    
    if not teams:
        print(f"No teams found matching '{team_name}'. \n")
    #Displays the matching teasm with their names and ID's

    print(f"\nTeams matching '{team_name}': ")
    for i, team in enumerate(teams, 1):
        print(f"  {i}. {team['name']} (ID: {team['id']})")
    
    #offers to look up standings for a specific league.
    show_standings = input("Would you like to look up standings for a specific league? (y/n): ").strip().lower()
    if show_standings == "y":
        try:
            league_id = int(input("Enter league ID: "))
            season = int(input("Enter season year: "))
        
        except ValueError:
            print("Invalid input.\n")
            return
    lookup_standings(api_key, league_id, season)

    if not teams:
        print(f"No teams found matching the name '{team_name}'.\n")
        return

def lookup_standings(api_key, league_id, season):
    """Fetch and display league standings from the Highlighty API."""
    try:
        response = requests.get(
            "https://volleyball.highlightly.net/standings",
            headers={"x-rapidapi-key": api_key},
            params={"leagueId": league_id, "season": season},
            )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"API request failed: {e}\n")
        return
    
    #Parses responses and extracts the standings groups

    data = response.json()
    groups = data.get("groups", [])
    league = data.get("league", {})

    if not groups:
        print("No standings found for this league/season.\n")
        return


    #displays a formatted standings table
    print(f"\n{'='*55}")
    print(f" {league.get('name', 'Unknown')} - {league.get('season', 'N/A')}")
    print(f"{'='*55}")
    print(f" {'Pos':<5}{'Team':<25}{'W':<5}{'L':<5}{'Pts':<5}")
    print(f"{'-'*50}")

    for group in groups:
        for entry in group.get("standings", []):
            team = entry.get("team", {})
            team_name = team.get("name", "Unknown")

            print(
                f"  {entry.get('position', '-'):<5}"
                f"{team_name:<25}"
                f"  {entry.get('wins', 0):<5}"
                f"  {entry.get('loses', 0):<5}"
                f"  {entry.get('points', 0):<5}"
            )
    print(f"{'='*55}\n")

def record_player(players):
    """Records stats for a player."""
    name = input("Enter player name:").strip()
    if not name:
        print("Player name cannot be empty.")
        return
    print(f"Recording stats for {name}:")

    stats = {}
    for category in ["kills", "errors", "attempts", "aces", "digs", "blocks", "sets_played"]:
        while True:
            try:
                value = int(input(f"  {category}: "))
                if value < 0:
                    print("  Value must be positive or 0.")
                    continue
                if category == "sets_played" and value < 1:
                    continue
                stats[category] = value
                break
            except ValueError:
                print("  Please enter a whole number.")
    players[name] = stats
    print(f"Stats recorded for {name}. \n")





def main():
    """Main program loop."""
    players = {}
    api_key = load_api_key()

    print("=" * 40)
    print("  Volleyball Stat Tracker")
    print("=" * 40)

    while True:
        print("1. Record player stats")
        print("2. View analytics")
        print("3. Save stats")
        print("4. Load stats")
        print("5. Look up pro team")
        print("6. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            record_player(players)
        
        elif choice == "2":
            view_analytics(players)
        
        elif choice == "3":
            save_stats(players)
        
        elif choice == "4":
            loaded = load_stats()
            if loaded is not None:
                players = loaded
        
        elif choice == "5":
            if api_key:
                lookup_team(api_key)
            else:
                print("No API key found. Add HIGHLIGHTLY_API_KEY to your .env file.\n")

        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")



if __name__ == "__main__":
    main()
