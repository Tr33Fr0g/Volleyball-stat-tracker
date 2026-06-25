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
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.\n")



if __name__ == "__main__":
    main()
