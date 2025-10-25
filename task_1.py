import hashlib

class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _get_hashes(self, item):
        hashes = []
        for i in range(self.num_hashes):
            hash_value = int (hashlib.md5(f"{item}{i}".encode()).hexdigest(), 16)
            hashes.append(hash_value % self.size)
        return hashes
    
    def add(self, item):
        if not isinstance(item, str) or not item.strip():
            return
        
        for h in self._get_hashes(item):
            self.bit_array[h] = 1

    def contains(self, item):
        if not isinstance(item, str) or not item.strip():
            return False

        return all(self.bit_array[h] == 1 for h in self._get_hashes(item))

    @staticmethod
    def check_password_uniqueness(bloom_filter, passwords):
        results = {}
        for password in passwords:
            if not isinstance(password, str) or not password.strip():
                results[password] = "incorrect password"
                continue

            if bloom_filter.contains(password):
                results[password] = "already used"
            else:
                bloom_filter.add(password)
                results[password] = "unique"    

        return results

if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwery123"]
    for password in existing_passwords:
        bloom.add(password)

    new_password_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = BloomFilter.check_password_uniqueness(bloom, new_password_to_check)

    for password, status in results.items():
        print(f"Password: '{password}' - {status}.")





        