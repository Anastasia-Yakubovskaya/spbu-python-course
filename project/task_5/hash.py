from collections.abc import MutableMapping
from typing import Any, Optional, Iterator, Tuple, List


class HashTable(MutableMapping):
    """
    A hash table implementation using double hashing for collision resolution.

    This class implements the MutableMapping interface, providing dictionary-like
    functionality with key-value pair storage and retrieval.

    Attributes:
        _size (int): Current size of the internal hash table
        _table (List[Optional[Tuple[Any, Any]]]): Internal storage array
        _count (int): Number of key-value pairs currently stored
    """

    def __init__(self, initial_size: int = 13) -> None:
        """
        Initialize the hash table.

        Parameters:
            initial_size (int): Initial size of the hash table. Defaults to 13.
        """
        self._size = initial_size
        self._table: List[Optional[Tuple[Any, Any]]] = [None] * self._size
        self._count = 0

    def _hash1(self, key: Any) -> int:
        """
        Compute the primary hash value for a key.

        Parameters:
            key (Any): Key to hash

        Returns:
            int: Primary hash index in range [0, size-1]
        """
        return hash(key) % self._size

    def _hash2(self, key: Any) -> int:
        """
        Compute the secondary hash value for collision resolution.

        Parameters:
            key (Any): Key to hash

        Returns:
            int: Secondary hash value in range [1, size-1]
        """
        return 1 + (hash(key) % (self._size - 1))

    def _probe_sequence(self, key: Any) -> Iterator[int]:
        """
        Generate a probe sequence using double hashing.

        Parameters:
            key (Any): Key to generate probe sequence for

        Yields:
            Iterator[int]: Sequence of indices to probe
        """
        h1 = self._hash1(key)
        h2 = self._hash2(key)

        for i in range(self._size):
            yield (h1 + i * h2) % self._size

    def _add(self, key: Any, value: Any) -> None:
        """
        Internal method to add or update a key-value pair.

        Parameters:
            key (Any): Key to add or update
            value (Any): Value to associate with the key
        """
        for index in self._probe_sequence(key):
            item = self._table[index]
            if item is None:
                self._table[index] = (key, value)
                self._count += 1
                return
            elif item[0] == key:
                self._table[index] = (key, value)
                return
        self._rehash()
        self._add(key, value)

    def _search(self, key: Any) -> Optional[Any]:
        """
        Internal method to search for a key.

        Parameters:
            key (Any): Key to search for

        Returns:
            Optional[Any]: Value associated with the key, or None if not found
        """
        for index in self._probe_sequence(key):
            item = self._table[index]
            if item is not None and item[0] == key:
                return item[1]
        return None

    def _remove(self, key: Any) -> bool:
        """
        Internal method to remove a key-value pair.

        Parameters:
            key (Any): Key to remove

        Returns:
            bool: True if key was found and removed, False otherwise
        """
        for index in self._probe_sequence(key):
            item = self._table[index]
            if item is not None and item[0] == key:
                self._table[index] = None
                self._count -= 1
                return True
        return False

    def _rehash(self) -> None:
        """
        Rehash the table to a larger size when load factor is too high.
        """
        old_table = self._table
        old_size = self._size

        self._size = self._size * 2 + 1
        self._table = [None] * self._size
        self._count = 0

        for item in old_table:
            if item is not None:
                self._add(item[0], item[1])

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Set a key-value pair using bracket notation.

        Parameters:
            key (Any): Key to set
            value (Any): Value to associate with the key
        """
        if self._count >= self._size * 0.75:
            self._rehash()
        self._add(key, value)

    def __getitem__(self, key: Any) -> Any:
        """
        Get a value by key using bracket notation.

        Parameters:
            key (Any): Key to retrieve

        Returns:
            Any: Value associated with the key

        Raises:
            KeyError: If the key is not found
        """
        value = self._search(key)
        if value is None:
            raise KeyError(key)
        return value

    def __delitem__(self, key: Any) -> None:
        """
        Delete a key-value pair using del operator.

        Parameters:
            key (Any): Key to delete

        Raises:
            KeyError: If the key is not found
        """
        if not self._remove(key):
            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """
        Check if a key exists in the hash table.

        Parameters:
            key (Any): Key to check

        Returns:
            bool: True if key exists, False otherwise
        """
        return self._search(key) is not None

    def __iter__(self) -> Iterator[Any]:
        """
        Iterate over all keys in the hash table.

        Yields:
            Iterator[Any]: Iterator of all keys
        """
        for item in self._table:
            if item is not None:
                yield item[0]

    def __len__(self) -> int:
        """
        Get the number of key-value pairs in the hash table.

        Returns:
            int: Number of elements
        """
        return self._count

    def add(self, key: Any, value: Any) -> None:
        """
        Explicit method to add a key-value pair.

        Parameters:
            key (Any): Key to add
            value (Any): Value to associate with the key
        """
        self[key] = value

    def find(self, key: Any) -> Optional[Any]:
        """
        Explicit method to find a value by key.

        Parameters:
            key (Any): Key to search for

        Returns:
            Optional[Any]: Value if found, None otherwise
        """
        return self._search(key)

    def remove(self, key: Any) -> bool:
        """
        Explicit method to remove a key-value pair.

        Parameters:
            key (Any): Key to remove

        Returns:
            bool: True if key was found and removed, False otherwise
        """
        return self._remove(key)
