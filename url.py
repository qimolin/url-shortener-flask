import re
import redis

class URL:
    
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    def generate_shortened_url(self, url):
        if self.__is_valid(url):

            # create key to hold ID incrementer
            url_id = self.redis.incr('url_counter')

            # save mapping
            shortened_url = self.__encode_base62(url_id)
            self.redis.set(shortened_url, url)

            return shortened_url
        else:
            return "Invalid URL"

    def __encode_base62(self, url_id):

        if url_id == 0: 
            return self.BASE62[0]

        arr = []
        while url_id:
            url_id, rem = divmod(url_id, len(self.BASE62))
            arr.append(self.BASE62[rem])

        # the representation is reversed to the correct order    
        arr.reverse()
        return ''.join(arr)

    def __is_valid(self, url):
        regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None