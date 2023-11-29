from typing import List, Tuple, Dict

class Text:
    def __init__(self, generated_content : str, concepts : list):
        self.generate_tokens(s = generated_content, concepts = concepts)

    def add_token(self, tag: str, content: str):
        # Adds a token as a tuple (tag, content) to the tokens list
        self.tokens.append( (tag, content) )


    def combine_words(self, words: List[str], base_position: int, length_of_group: int) -> str:
        # Combines words into a single string based on base_position and length_of_group
        combined_token = words[base_position]
        for i in range(1, length_of_group):
            if base_position + i < len(words):
                combined_token += " " + words[base_position + i]
            else:
                # Return an empty string if length_of_group exceeds available words
                return ""
        return combined_token

    def generate_tokens (self, s: str, concepts: Dict[str, str] ):
        # Initialize an empty list to store tokens (tag, content pairs)
        self.tokens: List[Tuple[str, str]] = []

        # Processes text 's' and adds tokens based on the 'concepts' mapping
        words = s.split()
        base_position = 0
        while base_position < len(words):
            # Check combinations of 1, 2, or 3 words for matches in concepts
            for length_of_group in [3, 2, 1]:
                combined_word = self.combine_words(words, base_position, length_of_group)
                if combined_word in concepts:
                    # Add a link token if the combined word is in concepts
                    self.add_token("link", combined_word)
                    base_position += length_of_group
                    break
                elif length_of_group == 1:
                    # Add a text token for individual words not in concepts
                    self.add_token("text", words[base_position])
            else:
                # Increment base_position by 1 if no match is found
                base_position += 1
