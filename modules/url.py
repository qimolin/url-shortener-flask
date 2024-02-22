import re
import redis

class URL:
    
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    
    def generate_shortened_url(self, url, user_id):
        if self.__is_valid(url):

            # create key to hold ID incrementer
            url_id = self.redis_client.incr('url_counter', 100)

            # save mapping from shortened URL to original URL
            shortened_url = self.__encode_base62(url_id)
            self.redis_client.set(shortened_url, url)

            # save mapping from shortened URL to user ID
            self.redis_client.set(f"user:{shortened_url}", user_id)

            return shortened_url
        else:
            return "Invalid URL"
        
    def get_original_url(self, shortened_url):
        return self.redis_client.get(shortened_url)

    def get_all_urls_by_user(self, user_id):
        keys = self.redis_client.keys('*')

        key_value_pairs = dict()
        for key in keys:
            shortened_url = None
            if key != 'url_counter' and not key.startswith('user'):
                shortened_url = key
            if user_id == self.redis_client.get(f"user:{shortened_url}"):
                original_url = self.redis_client.get(shortened_url)
                key_value_pairs[f'http://localhost:5000/{shortened_url}'] = original_url

        return key_value_pairs

    def is_owner(self, user_id, shortened_url):
        stored_user_id = self.redis_client.get(f"user:{shortened_url}")
        return user_id == stored_user_id
    
    def url_exists(self, shortened_url):
        return self.redis_client.get(shortened_url) != None
    
    def delete_all_urls_by_user(self, user_id):
        keys = self.redis_client.keys('*')
        current_url_counter = self.redis_client.get('url_counter')
        deleted = 0
        for key in keys:
            shortened_url = None
            if key != 'url_counter' and not key.startswith('user'):
                shortened_url = key
            if user_id == self.redis_client.get(f"user:{shortened_url}"):
                self.redis_client.delete(shortened_url)
                deleted += 1
                self.redis_client.delete(f"user:{shortened_url}")
        new_url_counter = int(current_url_counter) - (deleted * 100)
        self.redis_client.set('url_counter', new_url_counter)
        
        return "All URLs deleted"
    
    def delete_original_url(self, shortened_url):
        url = self.redis_client.get(shortened_url)
        if url == None:
            return "URL not found"
        self.redis_client.delete(shortened_url)
        current_url_counter = self.redis_client.get('url_counter')
        self.redis_client.set('url_counter', int(current_url_counter) - 100)
        return "URL deleted"
    
    def update_original_url(self, shortened_url, new_url):
        if (self.redis_client.get(shortened_url) == None):
            return "URL not found"
        if self.__is_valid(new_url):
            self.redis_client.set(shortened_url, new_url)
            return "URL updated"
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
        r'^(?:https?://)?'  # Optional http:// or https://
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # Domain
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # TLDs or domains
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IP address
        r'(?:\:\d+)?'  # Optional port
        r'(?:/?|\S+)$', re.IGNORECASE)
        return re.match(regex, url) is not None