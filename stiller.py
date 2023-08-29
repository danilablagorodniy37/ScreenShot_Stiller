import bs4
import requests
from time import sleep
import string
import random

# Constants
DEFAULT_IMAGE = "//st.prntscr.com/2023/07/24/0635/img/0_173a7b_211be8ff.png"  # link to the image that appears when the screenshot is not available
USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
HEADERS = {'User-Agent': USER_AGENT}
MAX_TRIES = 5  # avoid looping and limit the number of requests


def generate_random_path():
    """Generate a random path of 4-6 lowercase letters."""
    length = random.randrange(4, 6)  # 4-6 characters is best for finding links
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def fetch_random_image():
    """Fetch a random image from prnt.sc and return its URL."""
    tries = 0
    while tries < MAX_TRIES:
        url = f"https://prnt.sc/{generate_random_path()}"
        response = requests.get(url, headers=HEADERS)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        data = soup.find('div', class_="image-container image__pic js-image-pic")

        if not data:
            return None

        img = data.find("img").get("src")

        if img and img != DEFAULT_IMAGE:
            return url
        tries += 1
        sleep(0.5)
    return None


def main():
    # The final function outputs found links of screenshots to the console.
    # they are placed in a list, which makes it possible to further interact with them.
    valid_links = []
    for _ in range(100):
        image_link = fetch_random_image()
        if image_link:
            valid_links.append(image_link)
            print(image_link)


main()
