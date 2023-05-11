class Episode(object):
    def __init__(self, data: dict) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the instance of the class, and defines what attributes it has.


        :param self: Represent the instance of the class
        :param data: dict: Pass the data to the class
        :return: None, which is the default return value of any function that doesn't explicitly return something else
        """
        self.number: int = data.get('number')
        self.title: str = data.get('title')
        self.href: str = data.get('href')
        self.publish_time: str = data.get('publish_time')

    def __str__(self):
        """
        The __str__ function is the default human-readable representation of the object.
        This means that if you print an object, or convert it to a string for display,
        this function will be called. It should return a string.

        :param self: Represent the instance of the class
        :return: The title of the article
        """
        return self.title

    def __repr__(self):
        """
        The __repr__ function is used to compute the &quot;official&quot; string representation of an object.
        This is how you would make an object of the class, e.g., in this case:
        x = ComplexNumber(3.0,-4.5)

        :param self: Represent the instance of the class
        :return: The string representation of the object
        """
        return self.__str__()

    @staticmethod
    def get_episode_number(episode_str: str) -> int:
        """
        The get_episode_number function takes in a string representing an episode number and returns the integer value
        of that episode number. The function strips any newline characters from the input string, then removes leading
        zeros from the string (if there are any). Finally, it converts this remaining string to an integer and returns
        it.

        :param episode_str: str: Specify the type of the parameter
        :return: The episode number from an episode string
        """
        number_str = episode_str.replace('\n', '').strip()
        while number_str[0] == "0":
            number_str = number_str[1:]

        return int(number_str)


class RecentEpisode(object):
    def __init__(self, data: dict) -> None:
        """
        The __init__ function is called when the class is instantiated.
        It sets up the object with all of its properties and methods.


        :param self: Represent the instance of the class
        :param data: dict: Pass in the data from the json file
        :return: None, which is the default return value for functions
        :doc-author: Trelent
        """
        self.anime_title = data.get('title').strip()
        self.anime_href = data.get('href').strip()
        self.anime_rating: float = float(data.get('rating').strip())
        self.episode_number = Episode.get_episode_number(data.get('last_episode')['number'])
        self.episode_href = data.get('last_episode')['href'].strip()
        self.episode_publish_time = data.get('last_episode')['time'].replace('\n', '').strip()

    def __repr__(self):
        """
        The __repr__ function is the &quot;official&quot; string representation of an object.
        It's what you get when you type the object name into a Python console, or pass it to str().
        The goal of __repr__ is to be unambiguous: if eval(repr(x)) == x, then __repr__ should return a string that looks like a valid Python expression that could be used to recreate an object with the same value (given an appropriate environment). If this is not possible, a string formatted using %s formatting should be returned.

        :param self: Refer to the object itself
        :return: The anime title and episode number
        :doc-author: Trelent
        """
        return f'{self.anime_title} - {self.episode_number}'
