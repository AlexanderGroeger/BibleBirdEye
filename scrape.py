import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url_book_name(book_name):
    """Convert book name to URL-friendly format."""
    return book_name.lower().replace(" ", "-").replace("1", "i").replace("2", "ii").replace("3", "iii")

def scrape_chapters(url):
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # find all chapter sections (they begin with “#### Chapter N”)
    # After each chapter header, the following sibling lines (text) until next chapter
    rows = []

    # Each chapter section is wrapped in <div class="keep-together">
    chapter_blocks = soup.find_all("div", class_="keep-together")
    
    for block in chapter_blocks:
        # Get the chapter number from the <h4> tag
        h4 = block.find("h4")
        if not h4:
            continue
        h4_text = h4.get_text(strip=True)
        if not h4_text.startswith("Chapter"):
            continue

        chapter = h4_text.replace("Chapter", "").strip()

        # Loop through each <div> after the h4 (skip the h4 itself)
        for div in block.find_all("div"):
            verse_span = div.find("span")
            if not verse_span:
                continue

            reference = verse_span.get_text(strip=True).split(":")[-1]

            # Remove the verse span to get the remaining text
            verse_span.extract()
            heading = div.get_text(strip=True).lstrip(" -")

            rows.append({
                "chapter": chapter,
                "verse": reference,
                "heading": heading
            })

    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    
    from books import BOOKS_OF_THE_BIBLE

    URL = "https://bibletalk.tv/print/quizzes/headings/{book}/esv"

    book_dfs = []
    for book in BOOKS_OF_THE_BIBLE:
        print(f"Scraping {book}...")
        book_url = URL.format(book=get_url_book_name(book))
        
        df = scrape_chapters(book_url)
        df.insert(0, 'book', book)
        book_dfs.append(df)

    all_books_df = pd.concat(book_dfs, ignore_index=True)
    print(all_books_df.head())

    all_books_df.to_csv("headings.csv", sep="|", index=False)
