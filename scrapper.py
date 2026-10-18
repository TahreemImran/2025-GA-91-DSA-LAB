import requests
import pandas as pd
import threading

from urllib.parse import urlparse, parse_qs

from PyQt5.QtCore import QThread, pyqtSignal


class ScraperWorker(QThread):
    progress_changed = pyqtSignal(int, str)
    scraping_done = pyqtSignal(str, int)

    def __init__(self, search_url=None):
        super().__init__()

        self.search_url = search_url

        self.paused = threading.Event()
        self.paused.set()

        self.stopped = False

    def pause(self):
        self.paused.clear()

    def resume(self):
        self.paused.set()

    def stop(self):
        self.stopped = True
        self.paused.set()

    def run(self):
        all_books = []
        seen_books = set()
        target = 15000

        url = "https://openlibrary.org/search.json"

        queries = [
            "harry potter",
            "science",
            "history",
            "computer science",
            "mathematics",
            "fiction",
            "biology",
            "technology",
            "education",
            "literature"
        ]

        # Read the optional URL.

        if self.search_url:
            try:
                parsed = urlparse(self.search_url)

                allowed_hosts = [
                    "openlibrary.org",
                    "www.openlibrary.org"
                ]

                if (
                    parsed.scheme not in ("http", "https")
                    or parsed.netloc.lower() not in allowed_hosts
                    or parsed.path.rstrip("/") != "/search.json"
                ):
                    self.scraping_done.emit(
                        "Invalid URL.\nUse an Open Library Search API URL, "
                        "for example:\n"
                        "https://openlibrary.org/search.json?title=science",
                        -1
                    )
                    return

                url_parameters = parse_qs(parsed.query)

                custom_query = (
                    url_parameters.get("title", [""])[0]
                    or url_parameters.get("q", [""])[0]
                ).strip()

                if not custom_query:
                    self.scraping_done.emit(
                        "The URL must include a title or q search parameter.",
                        -1
                    )
                    return

                queries = [custom_query]

            except Exception as error:
                self.scraping_done.emit(
                    "URL error: " + str(error),
                    -1
                )
                return

        # Collect books.

        for query in queries:
            if self.stopped or len(all_books) >= target:
                break

            for page in range(1, 101):
                self.paused.wait()

                if self.stopped or len(all_books) >= target:
                    break

                params = {
                    "title": query,
                    "page": page,
                    "limit": 100,
                    "fields": (
                        "key,title,author_name,first_publish_year,"
                        "isbn,publisher,subject,language,"
                        "edition_count,number_of_pages_median"
                    )
                }

                try:
                    response = requests.get(
                        url,
                        params=params,
                        timeout=30
                    )

                    response.raise_for_status()

                    books = response.json().get("docs", [])

                    if not books:
                        break

                    for book in books:
                        self.paused.wait()

                        if self.stopped:
                            break

                        book_id = book.get("key")

                        if (
                            book_id
                            and book_id not in seen_books
                        ):
                            seen_books.add(book_id)

                            all_books.append({
                                "Book_ID": book_id,
                                "Title": book.get("title", ""),
                                "Author": ", ".join(
                                    book.get("author_name", [])
                                ),
                                "Year": book.get(
                                    "first_publish_year", ""
                                ),
                                "ISBN": ", ".join(
                                    book.get("isbn", [])[:3]
                                ),
                                "Publisher": ", ".join(
                                    book.get("publisher", [])[:3]
                                ),
                                "Subject": ", ".join(
                                    book.get("subject", [])[:5]
                                ),
                                "Language": ", ".join(
                                    book.get("language", [])
                                ),
                                "Edition_Count": book.get(
                                    "edition_count", ""
                                ),
                                "Pages": book.get(
                                    "number_of_pages_median", ""
                                )
                            })

                            self.progress_changed.emit(
                                len(all_books), query
                            )

                            if len(all_books) >= target:
                                break

                    if self.stopped or len(all_books) >= target:
                        break

                    if len(books) < 100:
                        break

                    self.paused.wait(1)

                except (
                    requests.RequestException,
                    ValueError
                ) as error:
                    print("Scraping error:", error)
                    break

        # Save collected books.

        try:
            if all_books:
                new_df = pd.DataFrame(all_books)

                try:
                    old_df = pd.read_csv("books_data.csv")

                    new_df = pd.concat(
                        [old_df, new_df],
                        ignore_index=True
                    )

                    new_df = new_df.drop_duplicates(
                        subset=["Book_ID"]
                    )

                except FileNotFoundError:
                    pass

                new_df.to_csv(
                    "books_data.csv",
                    index=False,
                    encoding="utf-8-sig"
                )

            try:
                total = len(
                    pd.read_csv("books_data.csv")
                )
            except FileNotFoundError:
                total = 0

            if self.stopped:
                status = "Scraping stopped."
            else:
                status = "Scraping finished."

            self.scraping_done.emit(
                status
                + "\nNew books collected: "
                + str(len(all_books))
                + "\nTotal books: "
                + str(total),
                total
            )

        except Exception as error:
            self.scraping_done.emit(
                "Error saving data: " + str(error),
                -1
            )