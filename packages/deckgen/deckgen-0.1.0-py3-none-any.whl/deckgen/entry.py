from deckgen.decks.base import DeckGen


def main():
    """
    Main function to run the DeckGen application.
    """
    input_text = "Sample input text for deck generation."
    deck_gen = DeckGen(input_text)
    generated_deck = deck_gen.generate_deck()
    
    for card in generated_deck:
        print(f"Front: {card['front']}, Back: {card['back']}")