import requests
import sqlite3

MIN_SHORT_URL_LEN = 5
BASE62_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE_URL = "https://short/"
DB_PATH = "urls.db"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_CHARS[0]
    
    result = []
    while num > 0:
        result.append(BASE62_CHARS[num % 62])
        num //= 62
    
    return "".join(reversed(result))

def decode_base62(code: str) -> int:
    result = 0
    for char in code:
        result = result * 62 + BASE62_CHARS.index(char)
    return result

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            long_url TEXT NOT NULL           
        )
    """)

    conn.commit()
    conn.close()

def shorten_url(long_url: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO urls (long_url) VALUES (?)", [long_url])
    row_id = cursor.lastrowid

    encoded = encode_base62(row_id)

    cursor.execute("UPDATE urls SET code = ? WHERE id = ?", [encoded, row_id])

    conn.commit()
    conn.close()

    return BASE_URL + encoded

def get_long_url(encoded: str) -> str | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT long_url from urls WHERE code = ?", [encoded])
    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None

def url_is_valid(url: str):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def main():
    url = input("Enter the url:\n")
    if url_is_valid(url):
        shorten_url(url)
    else:
        print("The given URL is not valid or doesn't exist")


if __name__ == "__main__":
    # main()
    init_db()
    print(get_long_url("1"))
    print(get_long_url("2"))