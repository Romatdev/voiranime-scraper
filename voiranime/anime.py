from datetime import datetime

from voiranime.episode import Episode


class Anime(object):
    def __init__(self, data: dict) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its properties and methods.


        :param self: Represent the instance of the class
        :param data: dict: Store the data from the api
        :return: None
        """
        self.native_title: str = data.get('native_title')
        self.romaji_title: str = data.get('romaji_title')
        self.english_title: str or None = data.get('english_title')
        self.note: float = data.get('note')
        self.type: str = data.get('type')
        self.status: str = data.get('status')
        self.studios: str = data.get('studios')
        self.start_date: datetime = data.get('start_date')
        self.genres: list[str] = data.get('genres')
        self.thumbnail: str = data.get('thumbnail')
        self.trailer: str = data.get('trailer')
        self.synopsis: str = data.get('synopsis')
        self.episodes: list[Episode] = data.get('episodes')

    def __str__(self) -> str:
        """
        The __str__ function is used to return a string representation of the object.
        This is what you see when you print an object, or convert it to a string using str().
        The __str__ function should return a human-readable representation of the object.

        :param self: Represent the instance of the class
        :return: The romaji_title if it is not none, otherwise returns &quot;pas de titre&quot;
        """
        return self.romaji_title if self.romaji_title is not None else "Pas de titre"

    def __repr__(self):
        """
        The __repr__ function is used to generate a string representation of an object.
        This function should return a string that, when passed to eval(), returns an equivalent object.
        The __repr__ function is called by the repr() built-in and by string conversions (reverse quotes)
        and text-mode file write operations.

        :param self: Represent the instance of the class
        :return: A string representation of the object
        """
        return self.__str__() + (self.english_title if self.english_title is not None else "")
