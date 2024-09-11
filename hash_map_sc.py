# Name: Matt Gallo
# OSU Email: gallomat@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/13/24
# Description: An implementation of a hash map that utilizes a dynamic array for storage and
# chaining for collision resolution using a singly linked list. Contains methods for put(),
# resize_table(), table_load(), empty_buckets(), get(), contains_key(), remove(),
# get_keys_and_values(), clear(), and find_mode().


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key:value pair in the hash map. If the given key already exists in the hash map,
        its associated value is replaced with the new value.
        """
        # If load factor >=1, double capacity
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Get hash and bucket
        hash = self._hash_function(key)
        index = (hash % self._capacity)
        bucket = self._buckets.get_at_index(index)
        if self.contains_key(key):
            node = bucket.contains(key)
            node.value = value
        else:
            # Insert key:value pair in bucket at hash
            bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying table. All existing key/value pairs are put into the new
        table by rehashing the hash table links. If new_capacity is not prime, it is changed to the next
        highest prime number.
        """
        # If new_capacity < 1, do nothing
        if new_capacity < 1:
            return

        # If new_capacity is not prime, change it to the next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        while (self._size / new_capacity) > 1.0:
            new_capacity = new_capacity * 2
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)


        # Create new underlying dynamic array with new_capacity
        da = DynamicArray()
        for _ in range(new_capacity):
            da.append(LinkedList())

        keyValues = self.get_keys_and_values()
        for val in range(keyValues.length()):
            pair = keyValues.get_at_index(val)
            key = pair[0]
            hash = self._hash_function(key)
            newIndex = (hash % new_capacity)
            bucket = da.get_at_index(newIndex)
            bucket.insert(key, pair[1])


        # Update hash table and capacity
        self._buckets = da
        self._capacity = new_capacity


    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0

        # Iterate through the buckets, checking the length of each linked list.
        # If a list is empty, increase count
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket.length() == 0:
                count += 1

        return count

    def get(self, key: str):
        """
        Returns the value associated with the given key.
        If the key is not in the hash map, the method returns None.
        """
        hash = self._hash_function(key)
        index = (hash % self._capacity)
        bucket = self._buckets.get_at_index(index)

        value = bucket.contains(key)
        if value is None:
            return None

        return value.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        An empty hash map does not contain any keys
        """
        hash = self._hash_function(key)
        index = (hash % self._capacity)
        bucket = self._buckets.get_at_index(index)

        if bucket.contains(key):
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        """
        hash = self._hash_function(key)
        index = (hash % self._capacity)
        bucket = self._buckets.get_at_index(index)

        if bucket.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns an array where each index contains a tuple of a key/value pair stored in the hash map.
        """
        keyValues = DynamicArray()

        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            bucket.insert('key', 0)

            node = bucket.contains('key')
            node = node.next
            while node is not None:
                keyValues.append((node.key, node.value))
                node = node.next
            bucket.remove('key')

        return keyValues

    def clear(self) -> None:
        """
        Clears the contents of the hash map, does not change the underlying hash table capacity.
        """
        # Iterate through the array and assign a blank LinkedList to each index
        for bucket in range(self._buckets.length() - 1):
            self._buckets.set_at_index(bucket, LinkedList())

        self._size = 0

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple containing the mode value(s) from the input array along with the frequency.
    """
    map = HashMap()

    max_frequency = 0
    for i in range(da.length()):
        value = da.get_at_index(i)
        frequency = map.get(value) or 0
        frequency += 1
        map.put(value, frequency)

        if frequency > max_frequency:
            max_frequency = frequency

    # Create a dynamic array to store the mode(s)
    mode_array = DynamicArray()

    for i in range(da.length()):
        value = da.get_at_index(i)
        if map.get(value) == max_frequency:
            # Check if value is already in mode_array
            already_in_array = False
            for j in range(mode_array.length()):
                if mode_array.get_at_index(j) == value:
                    already_in_array = True
                    break

            if not already_in_array:
                mode_array.append(value)

    return mode_array, max_frequency

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
