from datetime import datetime


def get_days_from_today(date_str):

    try:
        # Перетворюємо рядок у об'єкт datetime
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Отримуємо поточну дату
        today = datetime.today().date()

        # Обчислюємо різницю у днях
        delta = today - input_date

        return delta.days
    except ValueError as ve:
        # Обробка помилки неправильного формату дати
        raise ValueError(
            f"Неправильний формат дати: {date_str}. Очікується формат 'РРРР-ММ-ДД'.") from ve


# Приклад використання:
if __name__ == "__main__":
    test_date = "2021-10-09"
    try:
        days_difference = get_days_from_today(test_date)
        print(f"Кількість днів між {test_date} і сьогодні: {days_difference}")
    except ValueError as e:
        print(e)
