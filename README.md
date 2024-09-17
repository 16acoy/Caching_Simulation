**Cache System Project**

_Overview_

This project implements a cache system with various caching strategies: Cyclic Cache, Least Recently Used (LRU) Cache, Most Recently Used (MRU) Cache, and Least Frequently Used (LFU) Cache. These strategies are built to improve memory access efficiency by storing frequently accessed data in a cache to reduce memory lookups.

The caching mechanism is particularly useful for managing memory in performance-critical applications. This implementation simulates the interaction between a memory and a cache, allowing comparison of different cache strategies based on cache hit counts, memory hit counts, and performance over time.

_Features_

Caching Strategies: Four different caching strategies are implemented:

Cyclic Cache: Overwrites entries cyclically once the cache is full.
LRU Cache: Evicts the least recently used entry from the cache.
MRU Cache: Evicts the most recently used entry from the cache.
LFU Cache: Evicts the least frequently used entry from the cache.
Cache and Memory Simulation: The cache interacts with a memory system, and memory lookups are only performed when the desired data is not found in the cache.

Hit Counts and Efficiency: Track the number of cache hits (data found in the cache) and memory hits (data fetched from the memory) for each caching strategy.

_Class Descriptions_

Cache

Base class for all caching strategies.
Initializes the memory, cache array, cache size, and hit counts.
Provides basic methods such as get_cache_hit_count(), get_memory_request_count(), and lookup().

CyclicCache

Cyclic replacement strategy: When the cache is full, entries are replaced in a round-robin fashion.
Uses a cyclic pointer (next_slot) to determine the next location to store data.

LRUCache

Least Recently Used (LRU) strategy: Keeps track of the last use of each cache entry and evicts the least recently used entry when the cache is full.
Each entry in the cache has a LastUse value that is updated on every lookup.

MRUCache

Most Recently Used (MRU) strategy: Evicts the most recently used cache entry when the cache is full.
Similar to LRU but evicts the most recently accessed entry instead of the least recently accessed one.

LFUCache

Least Frequently Used (LFU) strategy: Tracks how often each entry in the cache is accessed and evicts the least frequently accessed entry when the cache is full.
Each cache entry keeps a Requests count that tracks the frequency of access.
