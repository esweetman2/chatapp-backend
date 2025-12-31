import requests
import httpx
from bs4 import BeautifulSoup

def fetch_page_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    with httpx.Client(timeout=10) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text


def get_html(url):

    try:
        req = requests.get(url=url)

        if req.status_code == 200:
            return req.content
        else:
            return f"Failed with status code {req.status_code} and message {req.text}"
    except Exception as e:
        return f"Exception with error {e}"
    

if __name__ == "__main__":
    # content = get_html("https://www.zola.com/wedding/ericandkat2026/event")
    # print(content)

    content = fetch_page_text("https://www.zola.com/wedding/ericandkat2026/event")
    print(content)