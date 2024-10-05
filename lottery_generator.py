import random

MAX_NUMBER = 100
MIN_NUMBER = 1


def get_numbers_ticket(
    min_num: int = MIN_NUMBER,
    max_num: int = MAX_NUMBER,
    quantity: int = 1
) -> list:

    # Валідація типів параметрів
    if not all(isinstance(arg, int) for arg in [min_num, max_num, quantity]):
        raise ValueError("Усі параметри повинні бути цілими числами.")

    # Валідація значень параметрів
    if min_num < MIN_NUMBER:
        raise ValueError(
            f"Мінімальне число повинно бути не менше {MIN_NUMBER}.")

    if max_num > MAX_NUMBER:
        raise ValueError(
            f"Максимальне число повинно бути не більше {MAX_NUMBER}.")

    if min_num > max_num:
        raise ValueError("Мінімальне число не може бути більше максимального.")

    available_numbers = max_num - min_num + 1
    if quantity < 1:
        raise ValueError("Кількість чисел повинна бути принаймні 1.")

    if quantity > available_numbers:
        raise ValueError(
            "Кількість чисел не може перевищувати кількість унікальних чисел у діапазоні.")

    # Генерація унікальних випадкових чисел
    ticket = random.sample(range(min_num, max_num + 1), quantity)

    return sorted(ticket)


# Приклад використання:
if __name__ == "__main__":
    test_cases = [
        {"min_num": 1, "max_num": 49, "quantity": 6},
        {"min_num": 50, "max_num": 10, "quantity": 5},
        {"min_num": 1, "max_num": 5, "quantity": 10},
        {"min_num": 1, "max_num": 2, "quantity": 2},  # Коректний виклик
        {"min_num": 1, "max_num": 2, "quantity": 3},  # Перевищення
        {"min_num": -5, "max_num": 10, "quantity": 3},  # Мінімум менше
        {"min_num": 1, "max_num": 101, "quantity": 5},  # Максимум більше
        {"min_num": "a", "max_num": 10, "quantity": 5},  # Некоректний тип
    ]

    for idx, params in enumerate(test_cases, start=1):
        try:
            lottery_numbers = get_numbers_ticket(**params)
            print(f"Тест {idx}: Ваші лотерейні числа: {lottery_numbers}")
        except ValueError as e:
            print(f"Тест {idx}: Помилка: {e}")
