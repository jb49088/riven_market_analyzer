import datetime
import sqlite3

import bs4
import requests

url = "https://riven.market/_modules/riven/showrivens.php"

params = {
    "platform": "ALL",
    "limit": 200,
    "recency": -1,
    "veiled": "false",
    "onlinefirst": "false",
    "polarity": "all",
    "rank": "all",
    "mastery": 16,
    "weapon": "Any",
    "stats": "Any",
    "neg": "all",
    "price": 99999,
    "rerolls": -1,
    "sort": "time",
    "direction": "ASC",
    "page": 1,
    "time": int(datetime.datetime.now().timestamp() * 1000),
}


def init_database(database):
    """Setup the database with a single listings table."""

    db_path = database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            seller TEXT NOT NULL,
            source TEXT NOT NULL,
            weapon TEXT NOT NULL,
            stat1 TEXT,
            stat2 TEXT,
            stat3 TEXT,
            stat4 TEXT,
            price INTEGER NOT NULL,
            scraped_at TIMESTAMP
        )
    """)

    return db_path, conn, cursor


def fetch_page(url, params):
    """Fetch and parse a page."""

    # Update time for cache busting
    params["time"] = int(datetime.datetime.now().timestamp() * 1000)

    r = requests.get(url, params=params)
    r.raise_for_status()
    return bs4.BeautifulSoup(r.text, "html.parser")


def get_total_count(url, params):
    """Extract total riven and page count."""

    soup = fetch_page(url, params)

    pagination_div = soup.select_one("div.pagination")

    if not pagination_div:
        return 0, 1

    total_rivens = int(pagination_div.select("b")[-1].text)
    total_pages = (total_rivens + params["limit"] - 1) // params["limit"]

    return total_rivens, total_pages


def parse_rivens(soup):
    """Parse all rivens on a page."""

    rivens = []

    for element in soup.select("div.riven"):
        # Get seller name
        seller_div = element.select_one("div.attribute.seller")
        if not seller_div:
            continue

        seller_name = seller_div.text.strip().split("\n")[0].strip()

        # Create normalized entry
        riven = {
            "id": f"rm_{element['id']}",
            "seller": seller_name,
            "source": "riven.market",
            "weapon": element["data-weapon"].lower().replace(" ", "_"),
            "stat1": element["data-stat1"],
            "stat2": element["data-stat2"],
            "stat3": element["data-stat3"],
            "stat4": element["data-stat4"],
            "price": int(element["data-price"]),
            "scraped_at": datetime.datetime.now().isoformat(),
        }
        rivens.append(riven)

    return rivens


def insert_batch(cursor, conn, rivens):
    """Insert a batch of listings into the database."""

    cursor.executemany(
        """
        INSERT OR REPLACE INTO listings
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        [
            (
                r["id"],
                r["seller"],
                r["source"],
                r["weapon"],
                r["stat1"],
                r["stat2"],
                r["stat3"],
                r["stat4"],
                r["price"],
                r["scraped_at"],
            )
            for r in rivens
        ],
    )
    conn.commit()


def display_stats(start_time, total_scraped, db_path):
    """Display runtime statistics."""

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print("\nScrape complete!")
    print(f"Total rivens scraped: {total_scraped}")
    print(f"Duration: {duration}")
    print(f"Listings table saved to: {db_path}")


def main(url, params):
    """One-time full scrape of riven.market for historical data."""

    db_path, conn, cursor = init_database("market.db")

    print("Fetching total count...")
    total_rivens, total_pages = get_total_count(url, params)
    print(f"Found {total_rivens} rivens total ({total_pages} pages)")

    page = 1
    total_scraped = 0
    start_time = datetime.datetime.now()

    while page <= total_pages:
        try:
            params["page"] = page

            soup = fetch_page(url, params)

            rivens = parse_rivens(soup)

            if rivens:
                insert_batch(cursor, conn, rivens)

                total_scraped += len(rivens)
                print(
                    f"Page {page}/{total_pages}: {len(rivens)} rivens (Total: {total_scraped})"
                )
            else:
                print(f"Page {page}/{total_pages}: No rivens found")

            page += 1

        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    conn.close()

    display_stats(start_time, total_scraped, db_path)


if __name__ == "__main__":
    try:
        main(url, params)
    except KeyboardInterrupt:
        print("Scraper interrupted")
