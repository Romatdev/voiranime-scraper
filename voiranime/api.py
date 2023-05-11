from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests import Response, RequestException, Session

from voiranime.anime import Anime
from voiranime.episode import RecentEpisode, Episode
from voiranime.urls import Urls


class Voiranime:
    def __init__(self, key: str) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines all its attributes.
        In this case, it takes a key as an argument and assigns it to self.key.

        :param self: Represent the instance of the class
        :param key:str: Set the cf_clearance cookie
        :return: None because it is a constructor
        """
        self.key: str = key
        self.session: Session = requests.Session()
        self.session.cookies.set("cf_clearance", self.key, domain="v3.voiranime.com")
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }

    def get_recent_episodes(self) -> list[RecentEpisode]:
        """
        The get_recent_episodes function returns a list of RecentEpisode objects.

        :param self: Refer to the current instance of a class
        :return: A list of recentepisode objects
        """
        url: str = Urls.BASE_URL
        response: Response = self.session.get(url)

        if response.status_code != 200:
            raise RequestException("Cloudfare n'a pas été bypass.")

        html: str = response.text
        soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")

        episodes: list[RecentEpisode] = []

        divs = soup.find("div", {'id': 'loop-content'}).find_all('div', {'page-item-detail'})
        for dv in divs:
            summary = dv.find('div', {'class': 'item-summary'})
            a = summary.find('a')
            href = a['href']
            title = a.text
            rating = summary.find('span', {'class': 'score'}).text
            last_ep_ = summary.find('div', {'class': 'chapter-item'})
            chapter = last_ep_.find('span', {'class': 'chapter'})
            last_ep = {
                "number": chapter.text,
                "href": chapter.find('a')['href'],
                "time": last_ep_.find('span', {'class': 'post-on'}).text
            }

            episodes.append(RecentEpisode({
                "title": title,
                "href": href,
                "rating": rating,
                "last_episode": last_ep
            }))

        return episodes

    def get_anime(self, slug: str) -> Anime:
        """
        The get_anime function takes a slug as an argument and returns an Anime object.
        The Anime object contains the following attributes:
            - trailer (str)
            - thumbnail (str)
            - note (float)

        :param self: Represent the instance of the class
        :param slug: str: Get the anime's slug
        :return: An anime object
        """
        url: str = Urls.ANIME_URL(slug)
        response: Response = self.session.get(url)

        if response.status_code != 200:
            raise RequestException("Cloudfare n'a pas été bypass.")

        html: str = response.text
        soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")

        tab_summary = soup.find("div", {"class": "tab-summary"})
        summary_image = tab_summary.find("div", {"class": "summary_image"})
        try:
            trailer = summary_image.find('iframe')['src']
        except TypeError:
            trailer = None
        thumbnail = summary_image.find('img')['src']
        summary_content = tab_summary.find("div", {"class": "post-content"})
        rating = float(summary_content.find('span', {"class": "score"}).text)
        items = summary_content.find_all('div', {"class": "post-content_item"})

        data = {
            "trailer": trailer,
            "thumbnail": thumbnail,
            "note": rating
        }

        for item in items:
            key = item.find('h5').text.lower().strip().replace(' ', '')
            value = item.find('div', {"class": "summary-content"}).text.strip()
            if key == "native":
                data['native_title'] = value
            elif key == "romaji":
                data['romaji_title'] = value
            elif key == "english":
                data['english_title'] = value
            elif key == "type":
                data['type'] = value
            elif key == "status":
                data['status'] = value
            elif key == "studios":
                data['studios'] = value
            elif key == "startdate":
                data['start_date'] = datetime.strptime(value, "%b %d, %Y").date()
            elif key == "genre(s)":
                data['genres'] = [genre.strip() for genre in value.split(',')]

        descriptionSummary = soup.find('div', {"class": "description-summary"})
        data['synopsis'] = descriptionSummary.text.strip()

        episodes: list = []

        episodesContainer = soup.find('ul', {"class": "version-chap"})
        eps = episodesContainer.find_all('li', {'class': 'wp-manga-chapter'})
        for ep in eps:
            a = ep.find('a')
            href = a['href']

            aContent = a.text
            number = Episode.get_episode_number(aContent.split("-")[-1].strip())
            title = a.text.strip()
            publish_time = ep.find('i').text.strip()

            episodes.append(Episode({
                "number": number,
                "title": title,
                "href": href,
                "publish_time": publish_time
            }))

        data['episodes'] = episodes

        return Anime(data)


api = Voiranime("kvfV6QDHWAdPpc1nhZGsz0GQbFio2KCYdqfbHFAsu_4-1683817984-0-160")

print(api.get_anime("one-piece").episodes)
