import os
import requests
import csv

output_directory = "books"
os.makedirs(output_directory, exist_ok=True)
log_file_path = "book_log.csv"

def book_exists_in_log(book_id):
    with open(log_file_path, "r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row and row[0] == str(book_id):
                return True
    return False

def download_book(book_id):
    if book_exists_in_log(book_id):
        print(f"Book with ID {book_id} already exists in the log file. Skipping download.")
        return

    download_url = f"https://www.gutenberg.org/ebooks/{book_id}.txt.utf-8"
    response = requests.get(download_url)

    if response.status_code == 200:
        book_title = download_url.split("/")[-1].replace(".txt.utf-8", "")
        author_line = next((line for line in response.text.splitlines() if line.startswith("Author:")), None)

        if author_line:
            author = author_line.replace("Author:", "").strip()
        else:
            author = "Unknown Author"

        title_line = next((line for line in response.text.splitlines() if line.startswith("Title:")), None)

        if title_line:
            title = title_line.replace("Title:", "").strip()
        else:
            title = "Title not found"

        language_line = next((line for line in response.text.splitlines() if line.startswith("Language:")), None)

        if language_line:
            language = language_line.replace("Language:", "").strip()
        else:
            language = "Language not found"

        output_filename = f"{book_id}#{title}#{author}#{language}.txt"
        output_path = os.path.join(output_directory, output_filename)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(response.text)

        with open(log_file_path, "a", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([book_id, title, author, language])

        print(f"Downloaded and saved '{title}' by {author} in {language} to '{output_path}'")
    else:
        print(f"Failed to download the book from {download_url}")

start_book_id = int(input("Enter the starting book ID: "))
end_book_id = int(input("Enter the ending book ID: "))

for book_id in range(start_book_id, end_book_id + 1):
    download_book(book_id)
