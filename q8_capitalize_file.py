"""Question 8. Capitalize words and count whitespace in the output file."""

import argparse
import re
from pathlib import Path


def uppercase_first_letter(word):
    for index, character in enumerate(word):
        if character.isalpha():
            return word[:index] + character.upper() + word[index + 1:]
    return word


def capitalize_file(source, destination):
    if source.resolve() == destination.resolve() or (
        destination.exists() and source.samefile(destination)
    ):
        raise ValueError("Use a different path for the output file.")

    # Keep original spaces, tabs, and line endings.
    with source.open("r", encoding="utf-8", newline="") as file:
        original_text = file.read()
    transformed = re.sub(
        r"\S+", lambda match: uppercase_first_letter(match.group()), original_text
    )
    with destination.open("w", encoding="utf-8", newline="") as file:
        file.write(transformed)

    return sum(character.isspace() for character in transformed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        whitespace_count = capitalize_file(args.source, args.destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Whitespace characters: {whitespace_count}")


if __name__ == "__main__":
    main()
