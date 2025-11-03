import pandas as pd
import re
from util import sample_less_likely

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

    data = pd.read_csv("headings.csv", sep="|")

    while True:
        book = input("Enter a book to memorize: ")
        if not isinstance(book, str):
            print("No book provided. Please try again.")
            continue

        book = book.strip().lower()
        
        if book not in data['book'].str.lower().values:
            print(f"Book '{book}' not found in data. Please try again.")
            continue
        
        book_headings = data[data["book"].str.lower()==book]
        break

    while True:
        progress_file = f"{book.replace(' ', '_')}_progress.csv"
        try:
            book_progress = pd.read_csv(progress_file)
            if book_progress.empty:
                raise FileNotFoundError
            break
        except FileNotFoundError:
            print(f"Progress file '{progress_file}' not found or empty. Initializing new progress.")
            book_progress = book_headings[['book', 'chapter', 'verse', 'heading']].copy()
            book_progress['attempts'] = 0
            book_progress['correct'] = 0
            book_progress.to_csv(progress_file, index=False)
            break
    
    try:
        while True:
            # Get a random row for the specified book
            row = book_headings.iloc[sample_less_likely(book_progress)]

            # Extract relevant fields
            # book = row['book']
            chapter = int(row['chapter'])
            verse = int(row['verse'])
            heading = row['heading']

            # Prompt user for a guess
            chapter_guess = input(f"'{heading}' is found in {book} ")
            if not chapter_guess:
                print("No input provided. Exiting...")
                break
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
