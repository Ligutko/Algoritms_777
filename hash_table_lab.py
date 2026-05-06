"""Лабораторна робота №7: Хеш-таблиці (варіант 2).

Дані: українські слова (рядки).
Розв'язання колізій: відкрите хешування (метод ланцюжків).
"""

from pathlib import Path


class Node:
    """Вузол однозв'язного списку для зберігання слова у ланцюжку."""

    def __init__(self, word: str):
        self.word = word
        self.next = None


class HashTable:
    """Хеш-таблиця з методом ланцюжків для обробки колізій."""

    def __init__(self, size: int):
        # Ініціалізуємо таблицю списком з None заданого розміру.
        self.size = size
        self.table = [None] * size

    def _hash(self, word: str) -> int:
        # Проста хеш-функція: сума кодів Unicode символів за модулем розміру таблиці.
        return sum(ord(char) for char in word) % self.size

    def insert(self, word: str) -> None:
        # Обчислюємо індекс для слова.
        index = self._hash(word)
        new_node = Node(word)

        # Якщо комірка порожня — вставляємо одразу.
        if self.table[index] is None:
            self.table[index] = new_node
            return

        # Інакше (колізія) — йдемо в кінець ланцюжка та додаємо новий вузол.
        current = self.table[index]
        while current.next is not None:
            current = current.next
        current.next = new_node

    def search(self, word: str) -> tuple[bool, int]:
        # Пошук слова у відповідному ланцюжку з підрахунком порівнянь.
        index = self._hash(word)
        comparisons = 0
        current = self.table[index]

        while current is not None:
            comparisons += 1
            if current.word == word:
                return True, comparisons
            current = current.next

        return False, comparisons

    def delete_starting_with(self, letter: str) -> None:
        # Видаляємо всі вузли, у яких слово починається на задану літеру.
        target_letter = letter.lower()

        for i in range(self.size):
            current = self.table[i]
            prev = None

            while current is not None:
                starts_with_target = current.word.lower().startswith(target_letter)

                if starts_with_target:
                    # Видалення голови ланцюжка.
                    if prev is None:
                        self.table[i] = current.next
                        current = self.table[i]
                    else:
                        # Видалення вузла із середини або кінця ланцюжка.
                        prev.next = current.next
                        current = prev.next
                else:
                    prev = current
                    current = current.next

    def display(self) -> None:
        # Візуальне відображення таблиці та ланцюжків у консолі.
        print("Поточний стан хеш-таблиці:")
        for i, node in enumerate(self.table):
            if node is None:
                print(f"[{i}]: None")
                continue

            chain = ""
            current = node
            while current is not None:
                chain += f" -> {current.word}"
                current = current.next
            print(f"[{i}]:{chain}")


def test_iteration_1() -> None:
    """Тест базової реалізації (Ітерація 1)."""

    print("=== ЛР №7: Хеш-таблиця (метод ланцюжків) ===")
    hash_table = HashTable(size=5)

    words = ["Сонце", "Місяць", "Зірка", "Небо", "Хмара", "Космос", "Планета"]

    print("Додаємо слова до таблиці:")
    for word in words:
        print(f"  Вставка: {word}")
        hash_table.insert(word)

    print()
    hash_table.display()


def test_iteration_2() -> None:
    """Тест реалізації Завдання 2 (пошук + видалення за першою літерою)."""

    print("=== ЛР №7: Ітерація 2 (пошук і видалення) ===")

    # 1) Створюємо файл зі словами засобами Python.
    words_path = Path(__file__).with_name("words.txt")
    words_to_write = [
        "Абстракція",
        "База",
        "Вектор",
        "Акумулятор",
        "Графік",
        "Адаптер",
        "Стек",
        "Черга",
        "Дерево",
        "Алгоритм",
        "Масив",
        "Функція",
        "Рекурсія",
    ]
    words_path.write_text("\n".join(words_to_write), encoding="utf-8")
    print(f"Файл зі словами створено: {words_path.name}")

    # 2) Зчитуємо слова з файлу у список.
    words = [line.strip() for line in words_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"Зчитано слів: {len(words)}")

    # 3) Створюємо таблицю розміром 7 і заповнюємо її.
    hash_table = HashTable(size=7)
    for word in words:
        hash_table.insert(word)

    print("\nТаблиця після заповнення:")
    hash_table.display()

    # 4) Пошук слова, яке є у таблиці.
    found_stack, comparisons_stack = hash_table.search("Стек")
    print("\nРезультат пошуку слова 'Стек':")
    print(f"  Знайдено: {found_stack}, порівнянь: {comparisons_stack}")

    # 5) Пошук слова, якого немає.
    found_space, comparisons_space = hash_table.search("Космос")
    print("Результат пошуку слова 'Космос':")
    print(f"  Знайдено: {found_space}, порівнянь: {comparisons_space}")

    # 6) Видаляємо всі слова, що починаються на 'А'.
    print("\nВидалення всіх слів на літеру 'А'...")
    hash_table.delete_starting_with("А")

    print("Таблиця після видалення:")
    hash_table.display()


def analyze_table(hash_table: "HashTable") -> dict:
    """Аналізує стан таблиці: к-ть колізій, макс. довжина ланцюжка, к-ть зайнятих кошиків."""
    collisions = 0          # кошики з ланцюжком довжини > 1
    max_chain = 0
    occupied_buckets = 0
    total_nodes = 0

    for node in hash_table.table:
        if node is None:
            continue
        occupied_buckets += 1
        chain_len = 0
        current = node
        while current is not None:
            chain_len += 1
            current = current.next
        total_nodes += chain_len
        if chain_len > 1:
            collisions += 1
        if chain_len > max_chain:
            max_chain = chain_len

    return {
        "size": hash_table.size,
        "occupied": occupied_buckets,
        "collisions": collisions,
        "max_chain": max_chain,
        "load_factor": total_nodes / hash_table.size if hash_table.size else 0,
    }


def compare_table_sizes(words: list, sizes: list, search_words: list, log_fn) -> None:
    """Виконує порівняння хеш-таблиць різних розмірностей.

    Для кожного розміру з sizes:
      - Будує хеш-таблицю.
      - Аналізує колізії та макс. довжину ланцюжка.
      - Шукає кожне слово зі search_words і фіксує кількість порівнянь.
      - Логує результат у вигляді таблиці.
    """
    log_fn("\n" + "=" * 78)
    log_fn("ПОРІВНЯННЯ ЕФЕКТИВНОСТІ ДЛЯ РІЗНИХ РОЗМІРНОСТЕЙ ТАБЛИЦІ")
    log_fn("=" * 78)
    log_fn(f"Загальна кількість слів у файлі: {len(words)}")
    log_fn(f"Слова для пошуку: {', '.join(search_words)}")

    # Заголовок таблиці
    header = f"{'Розмір':>7} | {'Зайн.':>6} | {'Колізій':>8} | {'MaxLen':>7} | {'Load':>6} | "
    header += " | ".join(f"{w:>10}" for w in search_words)
    log_fn("\n" + header)
    log_fn("-" * len(header))

    results = []
    for size in sizes:
        hash_table = HashTable(size=size)
        for word in words:
            hash_table.insert(word)

        stats = analyze_table(hash_table)

        # Пошук кожного слова — рахуємо порівняння
        comparisons_per_word = []
        for w in search_words:
            _, cmp_count = hash_table.search(w)
            comparisons_per_word.append(cmp_count)

        row = f"{stats['size']:>7} | {stats['occupied']:>6} | {stats['collisions']:>8} | "
        row += f"{stats['max_chain']:>7} | {stats['load_factor']:>6.2f} | "
        row += " | ".join(f"{c:>10}" for c in comparisons_per_word)
        log_fn(row)

        results.append({"size": size, "stats": stats, "comparisons": comparisons_per_word})

    # Висновки
    log_fn("\nВИСНОВКИ З ПОРІВНЯННЯ:")

    avg_comparisons = []
    for r in results:
        avg = sum(r["comparisons"]) / len(r["comparisons"])
        avg_comparisons.append((r["size"], avg, r["stats"]))

    best = min(avg_comparisons, key=lambda x: x[1])
    worst = max(avg_comparisons, key=lambda x: x[1])

    log_fn(f"  • Найгірший випадок: розмір = {worst[0]}")
    log_fn(f"      середня к-ть порівнянь = {worst[1]:.2f}")
    log_fn(f"      колізій = {worst[2]['collisions']}, макс. ланцюжок = {worst[2]['max_chain']}")

    log_fn(f"  • Найкращий випадок: розмір = {best[0]}")
    log_fn(f"      середня к-ть порівнянь = {best[1]:.2f}")
    log_fn(f"      колізій = {best[2]['collisions']}, макс. ланцюжок = {best[2]['max_chain']}")

    speedup = worst[1] / best[1] if best[1] else 0
    log_fn(f"  • Прискорення пошуку: x{speedup:.2f} разів")
    log_fn("=" * 78)


def test_final() -> None:
    """Фінальний інтерактивний запуск із дублюванням виводу в output.txt."""

    output_path = Path(__file__).with_name("output.txt")

    with output_path.open("w", encoding="utf-8") as output_file:
        def log(text: str = "") -> None:
            print(text)
            output_file.write(f"{text}\n")

        words_path = Path(__file__).with_name("words.txt")
        words = [
            line.strip()
            for line in words_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        log("=== ЛР №7: Фінальний запуск ===")
        log(f"Зчитано слів із {words_path.name}: {len(words)}")

        # 1. АВТОМАТИЧНЕ ПОРІВНЯННЯ РІЗНИХ РОЗМІРНОСТЕЙ (вимога ТЗ)
        sizes_to_test = [1, 3, 5, 7, 11, 15, 25]
        # Відбираємо реальні слова з файлу + перевіряємо неіснуюче для контрасту
        search_words = ["Стек", "Рекурсія", "Вектор", "Космос"]
        compare_table_sizes(words, sizes_to_test, search_words, log)

        # 2. ІНТЕРАКТИВНИЙ ЗАПУСК
        log("\n" + "=" * 78)
        log("ІНТЕРАКТИВНИЙ ЗАПУСК")
        log("=" * 78)

        size = int(input("\nВведіть розмір хеш-таблиці: "))
        hash_table = HashTable(size=size)
        for word in words:
            hash_table.insert(word)

        def log_table_state(title: str) -> None:
            log(title)
            log("Поточний стан хеш-таблиці:")
            for i, node in enumerate(hash_table.table):
                if node is None:
                    log(f"[{i}]: None")
                    continue

                chain_parts = []
                current = node
                while current is not None:
                    chain_parts.append(current.word)
                    current = current.next
                log(f"[{i}]: " + " -> ".join(chain_parts))

        log_table_state("\nТаблиця після заповнення:")

        search_word = input("Введіть слово для пошуку: ")
        found, comparisons = hash_table.search(search_word)
        log(f"\nРезультат пошуку слова '{search_word}':")
        log(f"  Знайдено: {found}, порівнянь: {comparisons}")

        letter = input("Введіть першу літеру для видалення: ")
        hash_table.delete_starting_with(letter)
        log_table_state(f"\nТаблиця після видалення слів на літеру '{letter}':")
        log(f"\nЛог збережено у файл: {output_path.name}")


if __name__ == "__main__":
    test_final()
