A volleyball stat tracker command line interface

A python command line interface software that is built for the main purpose of learning about github, uploading to the stardance challenge, and growth as a developer.

## Features

- **Statistic Recorder:** Records raw player stats and converts them with strong error handling features.
- **NCAA Linked Analytics System:** Instantaneously calculates hitting percentage, kill efficiency, per set averages and more.
- **Save/Load System:** Saves the stat sheets to a json local folder for future loading/use.
- **API Integration:** Uses the Highlightly API for professional team lookups and standings.
- **Comparison function:** Compares two players either on the current session or saved in JSONs head to head based on statistics.

## Install with pipx (recommended)

```bash
pipx install volleyball-tracker
```

This installs the `volleyball-tracker` command in an isolated environment, available anywhere on your machine.

## Setting up the Highlightly API key

Team lookups and standings (menu option 5) require a free API key from [Highlightly](https://highlightly.net/).

1. Sign up and grab your API key from Highlightly.
2. Set it as an environment variable named `HIGHLIGHTLY_API_KEY`, either:
   - In your shell:
     ```bash
     export HIGHLIGHTLY_API_KEY=your_actual_key
     ```
   - Or in a `.env` file in the directory you run the command from:
     ```
     HIGHLIGHTLY_API_KEY=your_actual_key
     ```

Without this key, everything except the pro team lookup/standings feature still works.

## Running the CLI

```bash
volleyball-tracker
```

## Running from source (development)

Clone the repository:

```bash
git clone https://github.com/your-username/volleyball-tracker.git
cd volleyball-tracker
pip install -e .
```

Create a `.env` file in the root directory and add your key:

```
HIGHLIGHTLY_API_KEY=your_actual_key
```

Run the application:

```bash
python tracker.py
```
