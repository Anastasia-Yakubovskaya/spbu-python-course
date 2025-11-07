import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_5")
sys.path.insert(0, os.path.abspath(project_path))

from hash import HashTable


def test_hash_table_basic_functionality():
    """
    Tests basic hash table operations.

    Verifies:
    - Element addition using [] operator
    - Element retrieval using [] operator
    - Updating existing elements
    - Element counting (__len__ method)
    """
    ht = HashTable()

    ht["apple"] = 5
    ht["banana"] = 10

    assert ht["apple"] == 5
    assert ht["banana"] == 10
    assert len(ht) == 2

    ht["apple"] = 15
    assert ht["apple"] == 15
    assert len(ht) == 2


def test_hash_table_contains_operator():
    """
    Tests the 'in' operator functionality.

    Verifies:
    - 'in' operator returns True for existing keys
    - 'in' operator returns False for non-existing keys
    """
    ht = HashTable()
    ht["key1"] = "value1"
    ht["key2"] = "value2"

    assert "key1" in ht
    assert "key2" in ht
    assert "key3" not in ht


def test_hash_table_deletion():
    """
    Tests element deletion operations.

    Verifies:
    - Element deletion using del operator
    - Deleted elements are properly removed
    - KeyError is raised when deleting non-existing elements
    """
    ht = HashTable()
    ht["a"] = 1
    ht["b"] = 2
    ht["c"] = 3

    del ht["b"]
    assert "b" not in ht
    assert len(ht) == 2

    try:
        del ht["nonexistent"]
        assert False
    except KeyError:
        pass


def test_hash_table_explicit_methods():
    """
    Tests explicit hash table methods.

    Verifies:
    - add() method for element addition
    - find() method for element search (returns None if not found)
    - remove() method for element deletion (returns boolean)
    """
    ht = HashTable()

    ht.add("x", 100)
    ht.add("y", 200)

    assert ht.find("x") == 100
    assert ht.find("y") == 200
    assert ht.find("z") is None

    assert ht.remove("x") is True
    assert ht.remove("nonexistent") is False
    assert ht.find("x") is None


def test_hash_table_collision_resolution():
    """
    Tests collision resolution using double hashing.

    Verifies:
    - Double hashing properly resolves collisions
    - All elements remain accessible after collisions
    - Values remain correct despite multiple collisions
    """
    ht = HashTable(initial_size=5)

    keys = ["a", "b", "c", "d", "e", "f", "g"]
    for i, key in enumerate(keys):
        ht[key] = i * 10

    for i, key in enumerate(keys):
        assert ht[key] == i * 10
        assert key in ht


def test_hash_table_rehashing():
    """
    Tests automatic rehashing behavior.

    Verifies:
    - Automatic rehashing when load factor exceeds threshold
    - Table size increases after rehashing
    - All elements remain accessible after rehashing
    """
    ht = HashTable(initial_size=5)
    initial_size = ht._size

    for i in range(10):
        ht[f"key_{i}"] = i

    assert ht._size > initial_size

    for i in range(10):
        assert ht[f"key_{i}"] == i


def test_hash_table_iteration():
    """
    Tests iteration over hash table keys.

    Verifies:
    - Proper iteration using for loop
    - All keys are returned during iteration
    - No duplicates in iteration results
    """
    ht = HashTable()
    test_data = {"k1": "v1", "k2": "v2", "k3": "v3"}

    for k, v in test_data.items():
        ht[k] = v

    iterated_keys = list(ht)

    assert set(iterated_keys) == set(test_data.keys())
    assert len(iterated_keys) == len(test_data)


def test_hash_table_edge_cases():
    """
    Tests edge cases and error conditions.

    Verifies:
    - KeyError when accessing non-existing elements
    - KeyError when deleting non-existing elements
    - Empty table behavior
    - Iteration over empty table
    """
    ht = HashTable()

    try:
        _ = ht["nonexistent"]
        assert False
    except KeyError:
        pass

    try:
        del ht["nonexistent"]
        assert False
    except KeyError:
        pass

    assert list(ht) == []
    assert len(ht) == 0
