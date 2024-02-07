import re

class URL:
    id = 0
    shortenedUrlDictionary = dict()

    def generate_shortened_url(self, url):
        if self.__is_valid(url):
            self.id += 1
            shortened_url = self.__encode_base62(url)
            self.shortenedUrlDictionary[shortened_url] = url
            return shortened_url
        else:
            return "Invalid URL"

    def __encode_base62(self, url):
        # TODO: Implement base62 encoding
        pass

    def __is_valid(self, url):
        regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None