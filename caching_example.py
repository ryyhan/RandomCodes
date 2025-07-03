import time

# A simple in-memory cache
cache = {}

def get_data_from_source(item_id):
    """Simulates fetching data from a slow data source."""
    print(f"Fetching item {item_id} from the data source...")
    time.sleep(2)  # Simulate a 2-second delay
    data = f"Data for item {item_id}"
    print(f"Finished fetching item {item_id}.")
    return data

def get_data(item_id):
    """
    Retrieves data for a given item_id.
    It first checks the cache. If the data is not in the cache,
    it fetches it from the source and stores it in the cache.
    """
    if item_id in cache:
        print(f"Getting item {item_id} from cache.")
        return cache[item_id]
    else:
        print(f"Item {item_id} not in cache.")
        data = get_data_from_source(item_id)
        cache[item_id] = data
        return data

if __name__ == "__main__":
    print("First call for item 1:")
    print(get_data(1))
    print("\n" + "="*20 + "\n")

    print("Second call for item 1 (should be faster):")
    print(get_data(1))
    print("\n" + "="*20 + "\n")

    print("First call for item 2:")
    print(get_data(2))
    print("\n" + "="*20 + "\n")

    print("Current cache state:")
    print(cache)
