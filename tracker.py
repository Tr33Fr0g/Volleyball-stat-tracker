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
        return f"value:.3f"

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
    print(f"Blocks/Set: {format_stat(analytics['aces_per_set'])}")
    print(f"Hitter Rating: {get_performance_rating(analytics['hitting_pct'])}")
    print(f"{'='*40}\n")


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
        
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")



if __name__ == "__main__":
    main()
