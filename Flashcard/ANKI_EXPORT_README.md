# Anki to Quizlet Export Script

This script helps export Anki flashcards as text files that can be imported into Quizlet.

> Note from GAchuzia: `anki_export_script.py` and this `README.md` are all Cursor code, and while I wan't to try and veer away from AI, I just needed a quick-fix for turning Anki cards -> Quizlet cards. My notes will not be AI generated, and neither will my flash cards, and I'll explicitly state when I do use AI.

## Prerequisites

### 1. Install AnkiConnect Add-on

1. Open Anki
2. Go to `Tools` > `Add-ons`
3. Click `Get Add-ons`
4. Enter this code: `2055492159`
5. Click `OK` and restart Anki

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Start Anki

Make sure Anki is running before using the script.

### 2. Run the Script

```bash
python anki_export_script.py
```

### 3. Choose Export Option

- __Option 1__: Export all decks
- __Option 2__: Export a specific deck
- __Option 3__: List available decks

## Output Format

The script creates `.txt` files in the `anki-decks/` directory. Each file contains flashcards in Quizlet's import format:

```txt
Front of card 1<TAB>Back of card 1
Front of card 2<TAB>Back of card 2
```

## Importing to Quizlet

1. Go to [Quizlet](https://quizlet.com) and log in
2. Click `Create` > `Study Set`
3. Enter a title for your set
4. Click `Import`
5. Copy and paste the content from your exported `.txt` file ([check anki-decks folder](flashcards\anki-decks))
6. Make sure the separator is set to `Tab`
7. Click `Import`

## Troubleshooting

### Connection Issues

- Make sure Anki is running
- Verify AnkiConnect add-on is installed and enabled
- Check that no firewall is blocking the connection

### Empty Exports

- Check that your deck contains cards
- Verify field names match the expected format (Front/Back, Question/Answer, etc.)

### Field Mapping

The script tries to automatically detect front/back fields. If your cards use different field names, you may need to modify the `export_deck_to_txt` method in the script.

## Notes

- HTML tags are automatically removed from card content
- Special characters are cleaned for Quizlet compatibility
- The script preserves UTF-8 encoding for international characters

This script provides a complete solution for exporting your Anki flashcards to Quizlet-compatible text files. Here's what it does:

## Key Features

1. __AnkiConnect Integration__: Uses the popular AnkiConnect add-on to communicate with Anki
2. __Automatic Field Detection__: Tries to identify front/back fields automatically
3. __HTML Cleaning__: Removes HTML tags and formats text for Quizlet import
4. __Flexible Export Options__: Export all decks or specific decks
5. __Quizlet-Compatible Format__: Outputs in the exact format Quizlet expects (tab-separated)

## To use this script

1. __Install AnkiConnect__ in Anki (add-on code: 2055492159)
2. __Install Python dependencies__: `pip install requests`
3. __Run the script__: `python anki_export_script.py`
4. __Import to Quizlet__: Copy the generated text files into Quizlet's import feature

The script will create `.txt` files in your `anki-decks/` folder that are ready to import into Quizlet. Each line will be formatted as `front<tab>back` which is exactly what Quizlet expects.
