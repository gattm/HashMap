# Name: Matt Gallo
# OSU Email: gallomat@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/13/24
# Description: An implementation of a hash map that utilizes a dynamic array for storage and
# Open Addressing with Quadratic Probing for collision resolution.
# Contains methods for put(),resize_table(), table_load(), empty_buckets(), get(), contains_key(), remove(),
# get_keys_and_values(), clear(), __iter__() and __next__().

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists in the hash map,
        its associated value is replaced with the new value. If the given key is not in the hash map,
        a new key/value pair is added.
        """
        # If load factor >=0.5, double capacity
        if self.table_load() >= 0.5:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Get hash and initial index
        hash = self._hash_function(key)
        initial = (hash % self._capacity)
        bucket = self._buckets.get_at_index(initial)
        # If index is empty, add HashEntry with key and value
        if bucket is None:
            self._buckets.set_at_index(initial, HashEntry(key, value))
        # If index is not empty, probe for empty position using Quadratic probing
        else:
            index = initial
            j = 1
            while bucket is not None and not bucket.is_tombstone:
                # If key matches key in HashMap, update associated value
                if bucket.key == key:
                    bucket.value = value
                    if bucket.is_tombstone:
                        bucket.is_tombstone = False
                    return
                index = (initial + j**2) % self._capacity
                j += 1
                bucket = self._buckets.get_at_index(index)
            # Set HashEntry at empty position
            self._buckets.set_at_index(index, HashEntry(key, value))

        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All active key/value pairs are put into the new table,
        and non-tombstone hash table links are rehashed.
        """
        # Check if new capacity is valid
        if new_capacity < self._size:
            return

        # Ensure new capacity is a prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new dynamic array with the new capacity
        new_buckets = DynamicArray()
        for _ in range(new_capacity):
            new_buckets.append(None)

        old_buckets, self._buckets = self._buckets, new_buckets
        self._capacity, old_capacity = new_capacity, self._capacity
        self._size = 0

        # Rehash all non-tombstone entries into the new table
        for index in range(old_capacity):
            entry = old_buckets.get_at_index(index)
            if entry is not None and not entry.is_tombstone:
                # Recalculate the new index for each entry
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the HashMap
        """
        count = 0
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket is None:
                count += 1
            elif bucket.is_tombstone:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. If the key is not in the hash map, returns None.
        """
        j = 1
        hash = self._hash_function(key)
        initial = (hash % self._capacity)
        bucket = self._buckets.get_at_index(initial)
        if bucket is None:
            return None
        else:
            while bucket is not None and not bucket.is_tombstone:
                if bucket.key == key:
                    if not bucket.is_tombstone:
                        return bucket.value
                else:
                    index = (initial + j**2) % self._capacity
                    bucket = self._buckets.get_at_index(index)
                    j += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the HashMap, otherwise returns False
        """
        if self._size == 0:
            return False
        j = 1
        hash = self._hash_function(key)
        initial = (hash % self._capacity)
        bucket = self._buckets.get_at_index(initial)
        if bucket is None:
            return False
        else:
            while bucket is not None and not bucket.is_tombstone:
                if bucket.key == key:
                    if not bucket.is_tombstone:
                        return True
                else:
                    index = (initial + j ** 2) % self._capacity
                    bucket = self._buckets.get_at_index(index)
                    j += 1

        return False


    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. If the key is not in the hash map,
        the method does nothing.
        """
        j = 1
        hash = self._hash_function(key)
        initial = (hash % self._capacity)
        bucket = self._buckets.get_at_index(initial)
        count = 0

        while bucket is not None and count < self._capacity:
            count += 1
            if bucket.key == key:
                if not bucket.is_tombstone:
                    self._size = (self._size - 1)
                    bucket.is_tombstone = True
            else:
                index = (initial + j ** 2) % self._capacity
                bucket = self._buckets.get_at_index(index)
                j += 1


    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the HashMap
        """
        keyValues = DynamicArray()
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket is not None:
                if not bucket.is_tombstone:
                    keyValues.append((bucket.key, bucket.value))

        return keyValues

    def clear(self) -> None:
        """
        Clears the contents of the HashMap, without changing the underlying hash table capacity
        """
        # Iterate through the array and assign None to each index
        for bucket in range(self._buckets.length()):
            self._buckets.set_at_index(bucket, None)

        self._size = 0

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            value = self._buckets.get_at_index(self._index)
            if value is None or value.is_tombstone:
                while value is None or value.is_tombstone:
                    self._index += 1
                    value = self._buckets.get_at_index(self._index)
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
