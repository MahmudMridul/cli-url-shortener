import requests

MIN_SHORT_URL_LEN = 5

def url_is_valid(url: str):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def shortened_url_is_valid(url: str):
    stripped = url.strip()
    if len(stripped) < MIN_SHORT_URL_LEN:
        print("Enter at least 5 characters")
        return False
    return True

def main():
    url = input("Enter the url:\n")
    if url_is_valid(url):
        shortened_url = input("Enter preferred shortened url:\n")

        if shortened_url_is_valid(shortened_url):
            print(shortened_url)
    else:
        print("The given URL is not valid or doesn't exist")


if __name__ == "__main__":
    main()
