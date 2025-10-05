#!/usr/bin/env python3
"""
Anki to Quizlet Export Script

This script connects to Anki via AnkiConnect and exports flashcards as text files
that can be imported into Quizlet.

Requirements:
1. Install AnkiConnect add-on in Anki
2. Install required Python packages: requests
3. Make sure Anki is running when you run this script

Usage:
    python anki_export_script.py
"""

import json
import requests
import os
from pathlib import Path
import re
from typing import List, Dict, Any

class AnkiExporter:
    def __init__(self, anki_connect_url: str = "http://localhost:8765"):
        """
        Initialize the Anki exporter.
        
        Args:
            anki_connect_url: URL where AnkiConnect is running (default: localhost:8765)
        """
        self.anki_connect_url = anki_connect_url
        
    def invoke(self, action: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Invoke an AnkiConnect action.
        
        Args:
            action: The action to perform
            params: Parameters for the action
            
        Returns:
            Response from AnkiConnect
        """
        request_data = {
            "action": action,
            "version": 6,
            "params": params or {}
        }
        
        try:
            response = requests.post(self.anki_connect_url, json=request_data)
            response.raise_for_status()
            result = response.json()
            
            if len(result) != 2:
                raise Exception("response has an unexpected number of fields")
            if "error" not in result:
                raise Exception("response is missing required error field")
            if "result" not in result:
                raise Exception("response is missing required result field")
            if result["error"] is not None:
                raise Exception(f"AnkiConnect error: {result['error']}")
                
            return result["result"]
            
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to Anki. Make sure Anki is running and AnkiConnect add-on is installed.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {e}")
    
    def get_deck_names(self) -> List[str]:
        """Get list of all deck names."""
        return self.invoke("deckNames")
    
    def get_notes_from_deck(self, deck_name: str) -> List[Dict[str, Any]]:
        """
        Get all notes from a specific deck.
        
        Args:
            deck_name: Name of the deck to export
            
        Returns:
            List of note data
        """
        # First, get all card IDs from the deck
        card_ids = self.invoke("findCards", {"query": f'deck:"{deck_name}"'})
        
        if not card_ids:
            print(f"No cards found in deck: {deck_name}")
            return []
        
        # Get note IDs from cards
        card_info = self.invoke("cardsInfo", {"cards": card_ids})
        note_ids = list(set(card["note"] for card in card_info))
        
        # Get note details
        notes_info = self.invoke("notesInfo", {"notes": note_ids})
        return notes_info
    
    def clean_html(self, text: str) -> str:
        """
        Remove HTML tags and clean up text for Quizlet import.
        
        Args:
            text: Text that may contain HTML
            
        Returns:
            Cleaned text
        """
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        # Replace HTML entities
        clean_text = clean_text.replace('&nbsp;', ' ')
        clean_text = clean_text.replace('&lt;', '<')
        clean_text = clean_text.replace('&gt;', '>')
        clean_text = clean_text.replace('&amp;', '&')
        clean_text = clean_text.replace('&quot;', '"')
        clean_text = clean_text.replace('&#39;', "'")
        # Clean up whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        # Remove newlines and tabs
        clean_text = clean_text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        return clean_text
    
    def export_deck_to_txt(self, deck_name: str, output_dir: str = "anki-decks") -> str:
        """
        Export a deck to a text file suitable for Quizlet import.
        
        Args:
            deck_name: Name of the deck to export
            output_dir: Directory to save the exported file
            
        Returns:
            Path to the exported file
        """
        print(f"Exporting deck: {deck_name}")
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Get notes from the deck
        notes = self.get_notes_from_deck(deck_name)
        
        if not notes:
            print(f"No notes found in deck: {deck_name}")
            return None
        
        # Prepare output file
        safe_deck_name = re.sub(r'[<>:"/\\|?*]', '_', deck_name)
        output_file = Path(output_dir) / f"{safe_deck_name}.txt"
        
        # Export notes to text file
        with open(output_file, 'w', encoding='utf-8') as f:
            for note in notes:
                fields = note.get("fields", {})
                
                # Extract front and back fields (adjust field names as needed)
                front = ""
                back = ""
                
                # Try common field names for front/back
                if "Front" in fields:
                    front = self.clean_html(fields["Front"]["value"])
                elif "Question" in fields:
                    front = self.clean_html(fields["Question"]["value"])
                elif "Term" in fields:
                    front = self.clean_html(fields["Term"]["value"])
                else:
                    # Use first field as front
                    field_names = list(fields.keys())
                    if field_names:
                        front = self.clean_html(fields[field_names[0]]["value"])
                
                if "Back" in fields:
                    back = self.clean_html(fields["Back"]["value"])
                elif "Answer" in fields:
                    back = self.clean_html(fields["Answer"]["value"])
                elif "Definition" in fields:
                    back = self.clean_html(fields["Definition"]["value"])
                else:
                    # Use second field as back
                    field_names = list(fields.keys())
                    if len(field_names) > 1:
                        back = self.clean_html(fields[field_names[1]]["value"])
                
                # Write card in Quizlet format (front\tback)
                if front and back:
                    f.write(f"{front}\t{back}\n")
                elif front:  # If only front is available, use it for both
                    f.write(f"{front}\t{front}\n")
        
        print(f"Exported {len(notes)} cards to: {output_file}")
        return str(output_file)
    
    def export_all_decks(self, output_dir: str = "anki-decks") -> List[str]:
        """
        Export all decks to text files.
        
        Args:
            output_dir: Directory to save the exported files
            
        Returns:
            List of exported file paths
        """
        deck_names = self.get_deck_names()
        exported_files = []
        
        print(f"Found {len(deck_names)} decks: {', '.join(deck_names)}")
        
        for deck_name in deck_names:
            try:
                output_file = self.export_deck_to_txt(deck_name, output_dir)
                if output_file:
                    exported_files.append(output_file)
            except Exception as e:
                print(f"Error exporting deck '{deck_name}': {e}")
        
        return exported_files

def main():
    """Main function to run the export script."""
    print("Anki to Quizlet Export Script")
    print("=" * 40)
    
    # Initialize exporter
    exporter = AnkiExporter()
    
    try:
        # Test connection to Anki
        print("Testing connection to Anki...")
        version = exporter.invoke("version")
        print(f"Connected to Anki version: {version}")
        
        # Get user choice
        print("\nWhat would you like to do?")
        print("1. Export all decks")
        print("2. Export specific deck")
        print("3. List available decks")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Export all decks
            exported_files = exporter.export_all_decks()
            print(f"\nExport complete! {len(exported_files)} files created:")
            for file_path in exported_files:
                print(f"  - {file_path}")
                
        elif choice == "2":
            # Export specific deck
            deck_names = exporter.get_deck_names()
            print(f"\nAvailable decks:")
            for i, deck_name in enumerate(deck_names, 1):
                print(f"  {i}. {deck_name}")
            
            try:
                deck_index = int(input(f"\nEnter deck number (1-{len(deck_names)}): ")) - 1
                if 0 <= deck_index < len(deck_names):
                    selected_deck = deck_names[deck_index]
                    output_file = exporter.export_deck_to_txt(selected_deck)
                    if output_file:
                        print(f"\nExport complete! File created: {output_file}")
                else:
                    print("Invalid deck number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == "3":
            # List decks
            deck_names = exporter.get_deck_names()
            print(f"\nAvailable decks ({len(deck_names)} total):")
            for i, deck_name in enumerate(deck_names, 1):
                print(f"  {i}. {deck_name}")
        else:
            print("Invalid choice.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Anki is running")
        print("2. Install AnkiConnect add-on in Anki")
        print("3. Check that AnkiConnect is enabled in Anki")

if __name__ == "__main__":
    main()
