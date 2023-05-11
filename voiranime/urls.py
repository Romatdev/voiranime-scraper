from urllib.parse import urljoin

from voiranime.config import VOIRANIME_VERSION


class Urls:
    BASE_URL = f"https://{VOIRANIME_VERSION}.voiranime.com/"
    ANIME_URL = lambda slug: urljoin(Urls.BASE_URL, f"anime/{slug}/")