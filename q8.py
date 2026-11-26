def capitalize_text(text):
    result = []
    whitespace_count = 0
    needs_capital = True

    for char in text:
        if char.isspace():
            whitespace_count += 1
            needs_capital = True

        elif needs_capital and char.isalpha():
            char = char.upper()
            needs_capital = False

        result.append(char)

    updated_text = "".join(result)
    return updated_text, whitespace_count


def main():
    with open("input.txt", "r", encoding="utf-8", newline="") as input_file:
        original_text = input_file.read()

    updated_text, whitespace_count = capitalize_text(original_text)

    with open("output.txt", "w", encoding="utf-8", newline="") as output_file:
        output_file.write(updated_text)

    print("Whitespace characters:", whitespace_count)


if __name__ == "__main__":
    main()