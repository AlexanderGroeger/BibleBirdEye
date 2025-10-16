import pandas as pd
import re

def normalize(reference):
    """
    Normalize a scripture reference to a standard format:
    - Strip spaces
    - Lowercase
    - Standardize spacing between book/chapter/verse
    """
    # Remove extra spaces
    reference = reference.strip()
    # Normalize case
    reference = reference.lower()
    # Remove multiple spaces and handle things like "1 john"
    reference = re.sub(r'\s+', ' ', reference)
    # Normalize formatting: ensure "book chapter:verse"
    match = re.match(r'(.+?)\s+(\d+):(\d+)', reference)
    if match:
        book = match.group(1).strip()
        chapter = match.group(2).lstrip("0")  # remove leading zeros
        verse = match.group(3).lstrip("0")
        return f"{book} {chapter}:{verse}"
    return None  # Invalid format

def validate(guess, answer):
    """
    Validate a guess against the correct answer.
    """
    norm_guess = normalize(guess)
    norm_answer = normalize(answer)
    
    if not norm_guess or not norm_answer:
        return False  # Invalid format

    return norm_guess == norm_answer

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="Scripture Reference Quiz")
    parser.add_argument('--book', type=str, default='genesis')
    args = parser.parse_args()
    book = args.book.lower()
    
    data = pd.read_csv("headings.csv", sep="|")
    book_headings = data[data["book"].str.lower()==book]
    try:
        while True:
            # Get a random row for the specified book
            row = book_headings.sample(n=1).iloc[0]

            # Extract relevant fields
            # book = row['book']
            chapter = int(row['chapter'])
            verse = int(row['verse'])
            heading = row['heading']

            # Prompt user for a guess
            chapter_guess = input(f"'{heading}' is found in {book} ")
            chapter_guess = int(chapter_guess.strip())
            
            if chapter_guess == chapter:
                print("Correct!")
            else:
                print(f"Incorrect! The correct answer is {book} {chapter}.")
            # answer = f"{book} {chapter}:{verse}"

            # Validate the guess
            # if validate(guess, answer):
            #     print("Correct!")
            # else:
            #     print(f"Incorrect! The correct answer is {book} {chapter}:{verse}.")

    except KeyboardInterrupt:
        print("Goodbye!")
