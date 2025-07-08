import time
import threading
from collections import OrderedDict

class TimedLRUCache:
    def __init__(self, max_size=5, ttl=10):
        """
        max_size: maximum number of items in cache
        ttl: time-to-live in seconds
        """
        self.cache = OrderedDict()
        self.ttl = ttl
        self.max_size = max_size
        self.lock = threading.Lock()

    def _is_expired(self, entry_time):
        return (time.time() - entry_time) > self.ttl

    def get(self, key, fallback_fn):
        """
        Returns cached value if valid, else uses fallback_fn to fetch, store and return it.
        """
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if not self._is_expired(timestamp):
                    print(f"Cache hit for {key}")
                    # Move to end to show it's recently used
                    self.cache.move_to_end(key)
                    return value
                else:
                    print(f"Cache expired for {key}")
                    del self.cache[key]

            print(f"Cache miss for {key}, fetching fresh data...")
            value = fallback_fn(key)
            self.cache[key] = (value, time.time())
            self.cache.move_to_end(key)

            if len(self.cache) > self.max_size:
                evicted = self.cache.popitem(last=False)  # Pop the least recently used item
                print(f"Evicted {evicted[0]} from cache")

            return value

# Simulated slow data source
def fetch_user_profile(user_id):
    print(f"Fetching data for user {user_id}...")
    time.sleep(1)
    return {"user_id": user_id, "name": f"User{user_id}", "profile": f"Profile of user {user_id}"}

# Main block
if __name__ == "__main__":
    cache = TimedLRUCache(max_size=3, ttl=5)  # small size and TTL for demo

    for i in [1, 2, 3]:
        print(cache.get(i, fetch_user_profile))

    print("\n-- Repeat access to item 2 --")
    print(cache.get(2, fetch_user_profile))

    print("\n-- Add item 4 (should evict least recently used: item 1) --")
    print(cache.get(4, fetch_user_profile))

    print("\n-- Wait for TTL to expire --")
    time.sleep(6)

    print("\n-- Access expired item (item 2) --")
    print(cache.get(2, fetch_user_profile))
