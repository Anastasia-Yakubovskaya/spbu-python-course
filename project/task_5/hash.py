from collections.abc import MutableMapping
from typing import Any, Optional, Iterator, Tuple, List
import multiprocessing
from multiprocessing import Manager
from multiprocessing.managers import SyncManager


class HashTable(MutableMapping):
    """
    A hash table implementation using double hashing for collision resolution.

    This class implements the MutableMapping interface, providing dictionary-like
    functionality with key-value pair storage and retrieval.

    Multiprocessing notes
    --------------------
    - A multiprocessing.Manager is created inside the constructor (not at module
      import time) so importing this module does not spawn new processes.
    - The manager provides:
        * manager.list used as the shared table
        * manager.Value used for a shared integer counter
        * manager.Lock for synchronizing operations
    """

    def __init__(
        self, initial_size: int = 13, manager: Optional[SyncManager] = None
    ) -> None:
        """
        Initialize the hash table.

        Parameters:
            initial_size (int): Initial size of the hash table. Defaults to 13.
            manager (Optional[SyncManager]): Optional multiprocessing.Manager-like
                instance (useful for injecting a manager in tests). If None, a new
                Manager() is created lazily here.
        """
        # Create manager inside __init__ to avoid starting processes at import time.
        # On Windows starting a Manager at import leads to spawn-time import issues.
        self._manager: SyncManager = manager if manager is not None else Manager()
        self._lock = self._manager.Lock()

        self._size: int = initial_size
        # Shared list of length _size. Each slot is either None or a manager.list([key, value]).
        self._table = self._manager.list([None] * self._size)
        # Shared integer counter (Value proxy)
        self._count = self._manager.Value("i", 0)

    def _hash1(self, key: Any) -> int:
        return hash(key) % self._size

    def _hash2(self, key: Any) -> int:
        # secondary hash in range [1, size-1]
        return 1 + (hash(key) % (self._size - 1))

    def _probe_sequence(self, key: Any) -> Iterator[int]:
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        for i in range(self._size):
            yield (h1 + i * h2) % self._size

    def _add(self, key: Any, value: Any) -> bool:
        """
        Insert or update under lock; returns True if inserted/updated, False if table
        is full (caller may choose to rehash and retry).
        """
        with self._lock:
            for index in self._probe_sequence(key):
                item = self._table[index]
                if item is None:
                    # store pair as manager.list so we can set item[1] later (if desired)
                    self._table[index] = self._manager.list([key, value])
                    self._count.value += 1
                    return True
                elif item[0] == key:
                    # update
                    item[1] = value
                    return True
            return False  # full

    def _search(self, key: Any) -> Optional[Any]:
        """
        Search for key under lock and return value or None if not found.
        """
        with self._lock:
            for index in self._probe_sequence(key):
                item = self._table[index]
                if item is not None and item[0] == key:
                    return item[1]
            return None

    def _remove(self, key: Any) -> bool:
        """
        Remove key under lock. Return True if removed, False if not found.
        """
        with self._lock:
            for index in self._probe_sequence(key):
                item = self._table[index]
                if item is not None and item[0] == key:
                    self._table[index] = None
                    self._count.value -= 1
                    return True
            return False

    def _rehash(self) -> None:
        """
        Rehash to a larger table while holding the lock.
        """
        with self._lock:
            old_table = list(self._table)
            old_items: List[Tuple[Any, Any]] = []
            for item in old_table:
                if item is not None:
                    old_items.append((item[0], item[1]))

            # increase size and create new shared list
            self._size = self._size * 2 + 1
            self._table = self._manager.list([None] * self._size)
            self._count.value = 0

            # reinsert
            for k, v in old_items:
                # use _add without acquiring lock again (we already hold it)
                # but _add acquires the lock; to avoid double-locking, call internal insertion
                # directly here (duplicate of _add's main logic without lock)
                for index in self._probe_sequence(k):
                    if self._table[index] is None:
                        self._table[index] = self._manager.list([k, v])
                        self._count.value += 1
                        break
                    # if collision - continue probing

    # MutableMapping API

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a key-value pair. Rehashes automatically when load factor >= 0.75.
        """
        # Acquire lock inside _add/_rehash; but check/rehash without extra races by locking here
        # (we re-acquire inside helpers; acceptable because they handle locking themselves)
        if self._count.value >= self._size * 0.75:
            self._rehash()
        success = self._add(key, value)
        if not success:
            # table was full unexpectedly; rehash and retry
            self._rehash()
            inserted = self._add(key, value)
            if not inserted:
                raise RuntimeError("Insertion failed even after rehash")

    def __getitem__(self, key: Any) -> Any:
        """
        Get a value by key. Raises KeyError if key not found.
        """
        value = self._search(key)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key: Any) -> None:
        """
        Delete an item by key. Raises KeyError if key not found.
        """
        if not self._remove(key):
            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Return True if key present, False otherwise.
        """
        return self._search(key) is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over keys. Snapshot of the table is taken to avoid holding lock during yield.
        """
        snapshot = list(self._table)
        for item in snapshot:
            if item is not None:
                yield item[0]

    def __len__(self) -> int:
        """
        Return number of stored elements.
        """
        return int(self._count.value)

    # convenience methods mirroring previous API

    def add(self, key: Any, value: Any) -> None:
        """Explicit add (same as __setitem__)."""
        self[key] = value

    def find(self, key: Any) -> Optional[Any]:
        """Explicit find (returns None if not found)."""
        return self._search(key)

    def remove(self, key: Any) -> bool:
        """Explicit remove (returns True if removed)."""
        return self._remove(key)
