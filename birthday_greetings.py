from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

DATE_FORMAT = "%Y.%m.%d"
DAYS_IN_WEEK = 7
MONDAY = 0  # Понеділок
WEEKEND_DAYS = [5, 6]  # Субота та Неділя


def adjust_for_leap_year(year: int, month: int, day: int) -> datetime.date:

    try:
        return datetime(year=year, month=month, day=day).date()
    except ValueError:
        if month == 2 and day == 29:
            adjusted_date = datetime(year=year, month=2, day=28).date()
            logging.warning(
                f"Переносимо 29 лютого на 28 лютого для року {year}. Новий день народження: {adjusted_date}")
            return adjusted_date
        else:
            raise


def get_upcoming_birthdays(users: list, today: datetime.date = None) -> list:

    if today is None:
        today = datetime.today().date()
    upcoming_birthdays = []
    logging.debug(f"Поточна дата: {today}")

    for user in users:
        name = user.get("name")
        birthday_str = user.get("birthday")

        # Перевірка наявності необхідних ключів
        if not name or not birthday_str:
            logging.warning(
                f"Пропущено користувача через відсутність імені або дати народження: {user}")
            continue

        # Розділення дати на рік, місяць, день
        try:
            year, month, day = map(int, birthday_str.split('.'))
        except (ValueError, AttributeError):
            logging.warning(
                f"Некоректний формат дати народження для користувача '{name}': {birthday_str}")
            continue

        # Отримання дати народження цього року
        try:
            birthday_this_year = adjust_for_leap_year(today.year, month, day)
        except ValueError:
            logging.warning(
                f"Некоректна дата для користувача '{name}': {birthday_str}")
            continue

        # Визначення наступної дати народження
        if birthday_this_year < today:
            try:
                birthday_next = adjust_for_leap_year(
                    today.year + 1, month, day)
            except ValueError:
                logging.warning(
                    f"Некоректна дата для користувача '{name}': {birthday_str}")
                continue
        else:
            birthday_next = birthday_this_year

        # Обчислення різниці у днях між днем народженням та сьогодні
        delta_days = (birthday_next - today).days
        logging.debug(f"Різниця у днях для '{name}': {delta_days}")

        # Перевірка, чи день народження випадає на наступні 7 днів включно
        if 0 <= delta_days <= DAYS_IN_WEEK:
            congratulation_date = birthday_next

            # Перевірка, чи день народження припадає на вихідний
            if congratulation_date.weekday() in WEEKEND_DAYS:
                days_to_monday = DAYS_IN_WEEK - congratulation_date.weekday()
                congratulation_date += timedelta(days=days_to_monday)
                logging.info(
                    f"День народження '{name}' припадає на вихідний. Переносимо привітання на понеділок: {congratulation_date.strftime(DATE_FORMAT)}")

                # Перевірка, чи перенесена дата все ще в межах 7 днів
                if (congratulation_date - today).days > DAYS_IN_WEEK:
                    logging.info(
                        f"Після переносу, дата привітання для '{name}' виходить за межі {DAYS_IN_WEEK} днів. Пропускаємо.")
                    continue

            # Форматування дати привітання у рядок
            congratulation_date_str = congratulation_date.strftime(DATE_FORMAT)
            logging.debug(
                f"Дата привітання для '{name}': {congratulation_date_str}")

            # Додавання до списку
            upcoming_birthdays.append({
                "name": name,
                "congratulation_date": congratulation_date_str
            })

    return upcoming_birthdays


if __name__ == "__main__":
    # Фіксована дата для тестування
    test_today = datetime(year=2024, month=10, day=5).date()

    users = [
        {"name": "Іван Петров", "birthday": "1990.10.04"},       # Вчора
        {"name": "Марія Іванова", "birthday": "1985.10.05"},     # Сьогодні
        {"name": "Олексій Коваленко", "birthday": "1992.10.06"},  # Завтра
        # Приклад переносу (на вихідний)
        {"name": "Богдан Сидоренко", "birthday": "1988.10.07"},  # Субота
        {"name": "Светлана Мороз", "birthday": "1995.10.06"},    # Неділя
        {"name": "Данило Левченко", "birthday": "1993.10.08"},   # Понеділок
        {"name": "Єва Мартинес", "birthday": "1991.10.09"},      # Вівторок
        {"name": "Франк Мур", "birthday": "1987.10.10"},         # Наступний рік
        {"name": "Грейс Тейлор", "birthday": "invalid_date"},    # Некоректна дата
        {"name": "", "birthday": "1990.10.03"},                  # Відсутнє ім'я
        {"name": "Генрі Вільсон"},                               # Відсутня дата
        # 29 лютого (невисокосний рік)
        {"name": "Ізабелла Гарсія", "birthday": "1994.02.29"},
    ]

    upcoming_birthdays = get_upcoming_birthdays(users, today=test_today)
    print("Список привітань на цьому тижні:", upcoming_birthdays)
