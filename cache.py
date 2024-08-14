from memory import Memory
import utilities


class Cache():

    # Returns the name of the caching strategy being used
    def name(self):
        return 'Cache'

    # Takes two parameters. Parameter memory is the "memory". Size is
    # a non-negative integer that indicates the size of the cache.
    def __init__(self, data, size=5):
        self.memory = Memory(data)
        self.cache_hit_count = 0
        self.cache_hit_flag = False
        self.size = size
        self.next_slot = 0
        self.cache_array = []
        for i in range(0, size):
            self.cache_array.append({-1: ''})

    # Returns information on the number of cache hit counts
    def get_cache_hit_count(self):
        return self.cache_hit_count

    # Returns information on the number of memory hit counts
    def get_memory_request_count(self):
        return self.memory.get_request_count()

    # Returns the cache hit flag
    def get_cache_hit_flag(self):
        return self.cache_hit_flag

    # Look up an address. Uses caching if appropriate.
    def lookup(self, address):
        return self.memory.lookup(address)


class CyclicCache(Cache):

    # Returns the name of the caching strategy being used
    def name(self):
        return 'Cyclic'

    # Takes two parameters. Parameter memory is the "memory". Size is
    # a non-negative integer that indicates the size of the cache.
    def __init__(self, data, size=5):
        super().__init__(data)

    # Look up an address. Uses caching if appropriate.
    def lookup(self, address):
        for entry in self.cache_array:
            # Check each cache dictionary key for address
            for key in entry:
                if key == address:
                    # Address and data desired is in the cache
                    self.cache_hit_count += 1
                    self.cache_hit_flag = True
                    return entry[key]
        # Not in cache - lookup then add to cache
        self.cache_hit_flag = False
        data_at_address = super().lookup(address)
        self.cache_array[self.next_slot] = {address: data_at_address}
        # Increment next slot to match cyclic strategy
        self.next_slot += 1
        if self.next_slot == self.size:
            self.next_slot = 0
        return data_at_address


class LRUCache(Cache):

    # Returns the name of the caching strategy being used
    def name(self):
        return 'LRU'

    # Takes two parameters. Parameter memory is the "memory". Size is
    # a non-negative integer that indicates the size of the cache.
    def __init__(self, data, size=5):
        super().__init__(data)
        self.cache_array = []
        for i in range(0, size):
            # Include LastUse key in dictionary to use for strategy
            self.cache_array.append({-1: '', 'LastUse': -1})

    # Look up an address. Uses caching if appropriate.
    def lookup(self, address):
        for entry in self.cache_array:
            # Check each cache dictionary key for address
            for key in entry:
                if key == address:
                    # Address and data desired is in the cache
                    self.cache_hit_count += 1
                    self.cache_hit_flag = True
                    entry['LastUse'] = 0
                    return entry[key]
                elif key != 'LastUse':
                    # Increment the LastUse value since not a cache hit
                    entry['LastUse'] = entry['LastUse'] + 1
        # Not in cache - lookup then add to cache
        data_at_address = super().lookup(address)
        self.cache_hit_flag = False
        # Get next slot to insert new data
        max_time_since_use = 0
        index_of_max_time = -1
        for i in range(len(self.cache_array)):
            entry = self.cache_array[i]
            for key in entry:
                if key == -1:
                    # Empty space in cache can be used
                    self.cache_array[i] = {
                        address: data_at_address,
                        'LastUse': 0
                    }
                    return data_at_address
                else:
                    # Need to evict an entry from cache
                    if key == 'LastUse':
                        if entry[key] > max_time_since_use:
                            # Update entry to evict
                            max_time_since_use = entry[key]
                            index_of_max_time = i
        # Add to cache at chosen index
        if index_of_max_time != -1:
            self.cache_array[index_of_max_time] = {
                address: data_at_address,
                'LastUse': 0
            }
        return data_at_address


class MRUCache(Cache):

    # Returns the name of the caching strategy being used
    def name(self):
        return 'MRU'

    # Takes two parameters. Parameter memory is the "memory". Size is
    # a non-negative integer that indicates the size of the cache.
    def __init__(self, data, size=5):
        super().__init__(data)
        self.cache_array = []
        for i in range(0, size):
            self.cache_array.append({-1: '', 'LastUse': -1})

    # Look up an address. Uses caching if appropriate.
    def lookup(self, address):
        for entry in self.cache_array:
            for key in entry:
                if key == address:
                    # Address and data desired is in the cache
                    self.cache_hit_count += 1
                    self.cache_hit_flag = True
                    entry['LastUse'] = 0
                    return entry[key]
                elif key != 'LastUse':
                    # Increment the LastUse value since not a cache hit
                    entry['LastUse'] = entry['LastUse'] + 1
        # Not in cache - lookup then add to cache
        data_at_address = super().lookup(address)
        self.cache_hit_flag = False
        # Get next slot to insert new data
        min_time_since_use = -1
        index_of_min_time = -1
        for i in range(len(self.cache_array)):
            entry = self.cache_array[i]
            for key in entry:
                if key == -1:
                    # Empty space in cache can be used
                    self.cache_array[i] = {
                        address: data_at_address,
                        'LastUse': 0
                    }
                    return data_at_address
                else:
                    # Need to evict an entry from cache
                    if key == 'LastUse':
                        if (entry[key] != -1 and
                                entry[key] < min_time_since_use):
                            # Update entry to evict
                            min_time_since_use = entry[key]
                            index_of_min_time = i
                        elif entry[key] != -1 and min_time_since_use == -1:
                            # Set default entry to evict as first entry
                            min_time_since_use = entry[key]
                            index_of_min_time = i
        # Add to cache at chosen index
        self.cache_array[index_of_min_time] = {
            address: data_at_address,
            'LastUse': 0
        }
        return data_at_address


class LFUCache(Cache):

    # Returns the name of the caching strategy being used
    def name(self):
        return 'LFU'

    # Takes two parameters. Parameter memory is the "memory". Size is
    # a non-negative integer that indicates the size of the cache.
    def __init__(self, data, size=5):
        super().__init__(data)
        self.cache_array = []
        for i in range(0, size):
            self.cache_array.append({-1: '', 'LastUse': -1, 'Requests': 1})

    # Look up an address. Uses caching if appropriate.
    def lookup(self, address):
        for entry in self.cache_array:
            for key in entry:
                if key == address:
                    self.cache_hit_count += 1
                    self.cache_hit_flag = True
                    entry['Requests'] += 1
                    return entry[key]
                elif key != 'LastUse' and key != 'Requests':
                    entry['LastUse'] = entry['LastUse'] + 1
        # Not in cache - lookup then add to cache
        data_at_address = super().lookup(address)
        self.cache_hit_flag = False
        # Get next slot to insert new data
        min_requests = -1
        index_of_min_requests = -1
        max_time_since_use = 0
        index_of_max_time = -1
        for i in range(len(self.cache_array)):
            entry = self.cache_array[i]
            for key in entry:
                if key == -1:
                    # Empty space in cache can be used
                    self.cache_array[i] = {
                        address: data_at_address,
                        'LastUse': 0,
                        'Requests': 1
                    }
                    return data_at_address
                else:
                    # Need to evict an entry from cache
                    if key == 'Requests':
                        if entry[key] < min_requests:
                            # Update entry to evict (least requests)
                            min_requests = entry[key]
                            index_of_min_requests = i
                            max_time_since_use = 0
                            index_of_max_time = -1
                        elif min_requests == -1:
                            # Set default entry to evict as first entry
                            min_requests = entry[key]
                            index_of_min_requests = i
                            max_time_since_use = entry['LastUse']
                            index_of_max_time = i
                        elif entry[key] == min_requests:
                            if entry['LastUse'] > max_time_since_use:
                                # Update entry to evict (first added)
                                max_time_since_use = entry['LastUse']
                                index_of_max_time = i
        # Add to cache at chosen index
        if index_of_max_time != -1:
            self.cache_array[index_of_max_time] = {
                address: data_at_address, 'LastUse': 0, 'Requests': 1
            }
        else:
            self.cache_array[index_of_min_requests] = {
                address: data_at_address, 'LastUse': 0, 'Requests': 1
            }
        return data_at_address
