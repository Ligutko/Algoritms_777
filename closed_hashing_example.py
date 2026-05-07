"""ПРИКЛАД 2: Програмна реалізація ЗАКРИТОГО хешування (лінійне пробування).

Окрема демонстрація для звіту — як працює альтернативний метод обробки колізій
у порівнянні з реалізованим методом ланцюжків (Variant 2).
"""

EMPTY = None
DELETED = "__DEL__"


class ClosedHashTable:
    """Хеш-таблиця з відкритою адресацією (лінійне пробування)."""

    def __init__(self, size: int):
        self.size = size
        self.table = [EMPTY] * size       # масив комірок
        self.used = [False] * size         # масив прапорів зайнятості
        self.count = 0                     # активні елементи

    def _hash(self, word: str) -> int:
        """Хеш-функція: сума Unicode кодів за модулем розміру таблиці."""
        return sum(ord(c) for c in word) % self.size

    def insert(self, word: str) -> bool:
        """Вставка слова з лінійним пробуванням."""
        if self.count >= self.size:
            print("[!] Таблиця переповнена.")
            return False

        bucket = self._hash(word)
        start = bucket

        # Лінійне пробування — шукаємо вільну або видалену комірку
        while self.used[bucket]:
            if self.table[bucket] == word:
                return False  # дублікати не вставляємо
            bucket = (bucket + 1) % self.size
            if bucket == start:
                return False  # кільцевий обхід — таблиця повна

        self.table[bucket] = word
        self.used[bucket] = True
        self.count += 1
        return True

    def search(self, word: str) -> tuple[bool, int]:
        """Пошук слова з підрахунком кількості порівнянь."""
        bucket = self._hash(word)
        start = bucket
        comparisons = 0

        while self.table[bucket] is not EMPTY:
            if self.used[bucket]:
                comparisons += 1
                if self.table[bucket] == word:
                    return True, comparisons
            bucket = (bucket + 1) % self.size
            if bucket == start:
                break
        return False, comparisons

    def delete(self, word: str) -> bool:
        """Видалення слова — позначає комірку константою DELETED."""
        bucket = self._hash(word)
        start = bucket

        while self.table[bucket] is not EMPTY:
            if self.used[bucket] and self.table[bucket] == word:
                self.used[bucket] = False
                self.table[bucket] = DELETED  # tombstone-маркер
                self.count -= 1
                return True
            bucket = (bucket + 1) % self.size
            if bucket == start:
                break
        return False

    def display(self) -> None:
        """Вивід таблиці на екран."""
        print("\n--- Закрите хешування (linear probing) ---")
        print(" Idx | Зайнята | Слово")
        print("-" * 35)
        for i in range(self.size):
            if self.table[i] is EMPTY:
                val, status = "—", "Ні"
            elif self.table[i] == DELETED:
                val, status = "[видалено]", "Ні"
            else:
                val, status = self.table[i], "Так"
            print(f" {i:3d} | {status:^7s} | {val}")
        print("-" * 35)
        print(f"Заповнено: {self.count}/{self.size} (Load: {self.count/self.size:.2f})")


# ── Демонстрація ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("ПРИКЛАД 2: ЗАКРИТЕ ХЕШУВАННЯ (linear probing)")
    print("=" * 50)

    ht = ClosedHashTable(size=11)

    words = ["Стек", "Черга", "Дерево", "Граф", "Список", "Масив"]
    for w in words:
        ht.insert(w)

    ht.display()

    # Пошук
    for w in ["Стек", "Купа"]:
        found, cmps = ht.search(w)
        status = "знайдено" if found else "не знайдено"
        print(f"\nПошук '{w}': {status} (порівнянь: {cmps})")

    # Видалення з tombstone
    print("\nВидалення слова 'Черга'...")
    ht.delete("Черга")
    ht.display()
